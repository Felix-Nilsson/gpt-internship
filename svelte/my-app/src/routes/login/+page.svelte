<script>
    import { Input, InputWrapper, Title, Group, Button, Stack } from '@svelteuidev/core';
    import { LockClosed, Person } from 'radix-icons-svelte';
    

    async function get_credentials() {

    
        //Give the server some breathing room
        console.log('Fetching credentials...')

        //Check
        const response = await fetch("http://localhost:5001/credentials");
        const data = await response.json();
        
        console.log(data);
    
    }

  </script>
  

   <div class="center-screen">
    <Group spacing="lg" direction="column">
        <Title order={1} variant='gradient' gradient={{from: 'blue', to: 'red', deg: 45}} style="font-size: 5rem">
            MedHelp
        </Title>

        <form on:submit|preventDefault={get_credentials}>
            <Stack>
            <Input 
                icon={Person} 
                placeholder="Användarnamn"
                radius="lg"
                size="xl"
            />

            <Input 
                type="password" 
                icon={LockClosed} 
                placeholder="Lösenord"
                radius="lg"
                size="xl"
            />

            <Button variant='gradient' gradient={{from: 'teal', to: 'blue', deg: 60}} radius="lg" size="xl" ripple type="submit">
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