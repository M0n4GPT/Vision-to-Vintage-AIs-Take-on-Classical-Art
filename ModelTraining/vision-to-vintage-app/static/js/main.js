// main.js

$(document).ready(function () {
    // Initial setup: hide all interactive elements
    $('.image-section').hide();
    $('.loader').hide();
    $('#result').hide();
    $('#btn-retry').hide();

    // Function to preview uploaded image
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview')
                  .attr('src', e.target.result)  // Set <img> src to data URL
                  .hide()
                  .fadeIn(650);
            };
            reader.readAsDataURL(input.files[0]);
        }
    }

    // When a file is selected, show preview and predict button
    $('#imageUpload').change(function () {
        $('.image-section').show();
        $('#btn-predict').show();
        $('#result').hide().empty();
        $('#btn-retry').hide();
        readURL(this);
    });

    // Handle click on "Stylize!" button
    $('#btn-predict').click(function () {
        var form_data = new FormData($('#upload-file')[0]);

        // Hide predict button and show loader spinner
        $(this).hide();
        $('.loader').show();

        // Send the image to server for style transfer
        $.ajax({
            type: 'POST',
            url: '/',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            success: function (data) {
                // Hide loader, display result HTML, show retry button
                $('.loader').hide();
                $('#result').html(data).fadeIn(600);
                $('#btn-retry').show();
            },
            error: function (xhr) {
                // Hide loader and display error message
                $('.loader').hide();
                $('#result')
                  .html('<p class="text-danger">Error: ' + xhr.responseText + '</p>')
                  .fadeIn(600);
            }
        });
    });

    // Handle click on "Try Another Image" button
    $('#btn-retry').click(function () {
        // Reset the upload form
        $('#upload-file')[0].reset();
        // Clear preview image
        $('#imagePreview').attr('src', '').hide();
        // Hide all sections and buttons
        $('.image-section').hide();
        $('#btn-predict').hide();
        $('#result').hide().empty();
        // Hide retry button itself
        $(this).hide();
    });
});
