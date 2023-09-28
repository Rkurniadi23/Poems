$(document).ready(function() {
    $("#openaiForm").on("submit", function(event) {
        event.preventDefault(); // Prevent the form from submitting the traditional way

        $.ajax({
            url: "/openai",
            method: "POST",
            data: $(this).serialize(), // Serialize form data
            success: function(data) {
                // Populate the "Poem Text" textarea with the received data
                $("#poem_text").val(data);
            },
            error: function() {
                $("#response").html("<div class='alert alert-danger'>An error occurred. Please try again.</div>");
            }
        });
    });
});