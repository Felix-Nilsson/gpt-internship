<script>

    last_fetched = 0;

    // Basically a constant loop that keeps checking if the conversation has been updated in the backend

    
    // Should be called when a query is submitted, so that it will keep checking until a new response is accessed, it will then stop until called again
    function check_for_messages() {

        conversation = []

        while(true) {
            
            new_time = 0;

            //Check
            
            
            if (new_time > last_fetched){
                
                conversation = 0;

                break;
            }
            
        }

        return conversation;
    }

</script>


