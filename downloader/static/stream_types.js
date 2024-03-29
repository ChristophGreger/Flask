window.onload = function() {
    // Get the stream_radio and quality_select elements
    var streamRadioSelect = document.querySelector('select[name="stream_radio"]');
    var qualitySelect = document.querySelector('select[name="quality_select"]');

    // Create a dictionary that maps the stream types to their corresponding option classes
    var optionClassForStreamType = {
        'only_audio': 'only_audio_option',
        'only_video': 'only_video_option',
        'video': 'video_option'
    };

    // Listen for changes on the stream_radio select element
    streamRadioSelect.addEventListener('change', function() {
        // Get the selected stream type
        var selectedStreamType = this.value;

        // Get the corresponding option class
        var optionClass = optionClassForStreamType[selectedStreamType];

        // Hide all options in the quality_select select element
        var allOptions = qualitySelect.querySelectorAll('option');
        allOptions.forEach(function(option) {
            option.style.display = 'none';
        });

        // Show only the options with the corresponding class
        var optionsToShow = qualitySelect.querySelectorAll('.' + optionClass);
        optionsToShow.forEach(function(option) {
            option.style.display = 'block';
        });

        // Select the first option with the corresponding class
        if (optionsToShow.length > 0) {
            optionsToShow[0].selected = true;
        }
    });

    // Trigger the change event initially to set the correct options
    streamRadioSelect.dispatchEvent(new Event('change'));
}