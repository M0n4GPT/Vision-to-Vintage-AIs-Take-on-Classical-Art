import json
from pathlib import Path
import logging
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class FeedbackCollector:
    def __init__(self, feedback_path: str):
        self.feedback_path = Path(feedback_path)
        self.feedback_path.parent.mkdir(parents=True, exist_ok=True)
        self.feedback_data = self._load_feedback()
        
    def _load_feedback(self) -> Dict:
        """Load existing feedback data"""
        if self.feedback_path.exists():
            with open(self.feedback_path, 'r') as f:
                return json.load(f)
        return {"feedback": []}
    
    def _save_feedback(self):
        """Save feedback data to file"""
        with open(self.feedback_path, 'w') as f:
            json.dump(self.feedback_data, f, indent=2)
    
    def add_feedback(self, style: str, rating: int, comments: Optional[str] = None):
        """Add new feedback entry"""
        try:
            feedback_entry = {
                "timestamp": datetime.now().isoformat(),
                "style": style,
                "rating": rating,
                "comments": comments
            }
            self.feedback_data["feedback"].append(feedback_entry)
            self._save_feedback()
            logger.info(f"Feedback added for style {style}")
        except Exception as e:
            logger.error(f"Error adding feedback: {str(e)}")
            raise
    
    def get_style_analysis(self, style: str) -> Dict:
        """Get analysis for a specific style"""
        style_feedback = [
            f for f in self.feedback_data["feedback"]
            if f["style"] == style
        ]
        
        if not style_feedback:
            return {
                "style": style,
                "total_feedback": 0,
                "average_rating": 0,
                "rating_distribution": {i: 0 for i in range(1, 6)}
            }
        
        ratings = [f["rating"] for f in style_feedback]
        rating_dist = {i: ratings.count(i) for i in range(1, 6)}
        
        return {
            "style": style,
            "total_feedback": len(style_feedback),
            "average_rating": sum(ratings) / len(ratings),
            "rating_distribution": rating_dist,
            "comments": [f["comments"] for f in style_feedback if f["comments"]]
        }
    
    def get_all_analysis(self) -> Dict:
        """Get analysis for all styles"""
        styles = set(f["style"] for f in self.feedback_data["feedback"])
        return {
            style: self.get_style_analysis(style)
            for style in styles
        } 