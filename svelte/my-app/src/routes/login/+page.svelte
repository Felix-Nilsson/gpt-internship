<script>
    import { Input, InputWrapper, Title, Group, Button, Stack } from '@svelteuidev/core';
    import { LockClosed, Person } from 'radix-icons-svelte';
    import { navigate } from 'svelte-routing';
    import { goto } from '$app/navigation'
    
    const timer = ms => new Promise(res => setTimeout(res,ms))
    let login_result = false;
    

    async function get_credentials() {

    
        //Give the server some breathing room
        console.log('Fetching credentials...')

        //Check
        const response = await fetch("http://localhost:5001/credentials/get", {
            mode:"cors",
            method: "GET"});
        const data = await response.json();

        let result = data['success'];
        login_result = result;


    }
    const navigateToPage = () => {
    // Call the navigate function inside the const function
    navigate('/chat',{replace:true});
  };

    const handleSubmit = async (e) => {

        //data contains the input
        let data = new FormData(e.target);
        console.log(data)
        fetch("http://localhost:5001/credentials", {
            mode:"cors",
            method: "POST",
            body: JSON.stringify({'username': data.get("usernamefield"), "password":data.get("passwordfield")}),
            headers: {"Content-type": "application/json; charset=UTF-8"}
        });

       // await timer(3000)

        await get_credentials();

        
        console.log("log: " + login_result)
        if (login_result == true){
            //navigateToPage()
            goto("/chat")
        }
    }




  </script>
  

   <div class="center-screen">
    <Group spacing="lg" direction="column">
        <Title order={1} variant='gradient' gradient={{from: 'blue', to: 'red', deg: 45}} style="font-size: 5rem">
            MedHelp
        </Title>

        <form on:submit|preventDefault={handleSubmit}>
            <Stack>
            <Input 
                icon={Person} 
                placeholder="Användarnamn"
                name="usernamefield"
                radius="lg"
                size="xl"
            />

            <Input 
                type="password" 
                icon={LockClosed} 
                placeholder="Lösenord"
                name="passwordfield"
                radius="lg"
                size="xl"
            />

            <Button 
                variant='gradient' 
                gradient={{from: 'teal', to: 'blue', deg: 60}} 
                radius="lg" size="xl" 
                ripple 
                type="submit"
            >
                Skicka
            </Button>


            </Stack>


        </form>
        

    </Group>
</div>

<head>
<style>
    .center-screen {
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  min-height: 100vh;
}

    .button {
  padding-top: 50px;
  padding-right: 30px;
  padding-bottom: 50px;
  padding-left: 80px;
}


</style>
</head>