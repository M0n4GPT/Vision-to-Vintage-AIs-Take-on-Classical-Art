"""
Dashboard for monitoring data and label drift in production.
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import json
import asyncio
import plotly.graph_objects as go
from pathlib import Path
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class DriftDashboard:
    """Dashboard for monitoring drift metrics in production environment."""
    
    def __init__(self, app: FastAPI, metrics_path: str):
        """
        Initialize the drift dashboard.
        
        Args:
            app: FastAPI application instance
            metrics_path: Path to drift metrics JSON file
        """
        self.app = app
        self.metrics_path = Path(metrics_path)
        self.connections: set[WebSocket] = set()
        
        # Register routes
        self.app.get("/drift-dashboard")(self.serve_dashboard)
        self.app.websocket("/ws/drift-metrics")(self.websocket_endpoint)
        
        # Start background task for broadcasting metrics
        self.app.add_event_handler("startup", self.start_broadcasting)
    
    async def serve_dashboard(self) -> HTMLResponse:
        """Serve the drift dashboard HTML page."""
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Drift Monitoring Dashboard</title>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .container { max-width: 1200px; margin: 0 auto; }
                .metrics { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; }
                .metric-card { background: #f5f5f5; padding: 15px; border-radius: 5px; }
                .plot-container { margin-top: 20px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Drift Monitoring Dashboard</h1>
                <div id="metrics" class="metrics"></div>
                <div id="plot" class="plot-container"></div>
            </div>
            <script>
                const ws = new WebSocket(`ws://${window.location.host}/ws/drift-metrics`);
                const metricsDiv = document.getElementById('metrics');
                const plotDiv = document.getElementById('plot');
                
                ws.onmessage = function(event) {
                    const data = JSON.parse(event.data);
                    updateMetrics(data);
                    updatePlot(data);
                };
                
                function updateMetrics(data) {
                    let html = '';
                    for (const [metric, value] of Object.entries(data)) {
                        if (metric !== 'plot') {
                            html += `
                                <div class="metric-card">
                                    <h3>${metric}</h3>
                                    <p>${JSON.stringify(value, null, 2)}</p>
                                </div>
                            `;
                        }
                    }
                    metricsDiv.innerHTML = html;
                }
                
                function updatePlot(data) {
                    if (data.plot) {
                        Plotly.newPlot(plotDiv, data.plot.data, data.plot.layout);
                    }
                }
            </script>
        </body>
        </html>
        """
        return HTMLResponse(content=html_content)
    
    async def websocket_endpoint(self, websocket: WebSocket):
        """Handle WebSocket connections."""
        await websocket.accept()
        self.connections.add(websocket)
        try:
            while True:
                await websocket.receive_text()
        except WebSocketDisconnect:
            self.connections.remove(websocket)
    
    async def start_broadcasting(self):
        """Start broadcasting drift metrics to connected clients."""
        asyncio.create_task(self.broadcast_metrics())
    
    async def broadcast_metrics(self):
        """Broadcast latest drift metrics to all connected clients."""
        while True:
            try:
                metrics = self._get_latest_metrics()
                if metrics:
                    plot = self.create_metrics_plot(metrics)
                    data = {
                        **metrics,
                        'plot': plot
                    }
                    for connection in self.connections:
                        try:
                            await connection.send_json(data)
                        except WebSocketDisconnect:
                            self.connections.remove(connection)
            except Exception as e:
                logger.error(f"Error broadcasting metrics: {str(e)}")
            await asyncio.sleep(5)  # Update every 5 seconds
    
    def _get_latest_metrics(self) -> Optional[Dict[str, Any]]:
        """Get the latest drift metrics from the JSON file."""
        try:
            if self.metrics_path.exists():
                with open(self.metrics_path, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error reading metrics file: {str(e)}")
        return None
    
    def create_metrics_plot(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create an interactive plot of drift metrics.
        
        Args:
            metrics: Dictionary containing drift metrics
            
        Returns:
            Dictionary containing Plotly figure data
        """
        # Extract metric values
        ks_pvalue = metrics.get('ks_test', {}).get('p_value', 0)
        chi_pvalue = metrics.get('chi_square', {}).get('p_value', 0)
        wasserstein = metrics.get('wasserstein_distance', 0)
        pca_drift = metrics.get('pca_drift_score', 0)
        
        # Create traces
        traces = [
            go.Bar(
                name='K-S Test p-value',
                x=['K-S Test'],
                y=[ks_pvalue],
                marker_color='blue'
            ),
            go.Bar(
                name='Chi-Square p-value',
                x=['Chi-Square'],
                y=[chi_pvalue],
                marker_color='green'
            ),
            go.Bar(
                name='Wasserstein Distance',
                x=['Wasserstein'],
                y=[wasserstein],
                marker_color='red'
            ),
            go.Bar(
                name='PCA Drift Score',
                x=['PCA'],
                y=[pca_drift],
                marker_color='purple'
            )
        ]
        
        # Create layout
        layout = go.Layout(
            title='Drift Metrics',
            xaxis_title='Metric',
            yaxis_title='Value',
            barmode='group',
            showlegend=True
        )
        
        return {
            'data': traces,
            'layout': layout
        } 