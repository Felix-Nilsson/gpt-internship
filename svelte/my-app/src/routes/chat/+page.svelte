<script>
    import { Group, Title, Paper, ThemeIcon,
         Input , Button, Center, Burger, Navbar, Header, Stack, Divider} from '@svelteuidev/core';
    import Icon from '@iconify/svelte';
    import Conversation from "./Conversation.svelte";
    import { onMount } from 'svelte';

    let opened = false;

    let credentials = {};
    //Backend should be running on port 5001
    const DATA_URL = 'http://localhost:5001/data';

    const CREDENTIALS_URL = 'http://localhost:5001/credentials/get'

    let update_conversation;

    const handleSubmit = async (e) => {

        //data contains the input
        let data = new FormData(e.target);

        await fetch(DATA_URL, {
            method: "POST",
            body: JSON.stringify({'prompt': data.get('prompt')}),
            headers: {"Content-type": "application/json; charset=UTF-8"}
        });

		//Start looking for a response
		await update_conversation();
	}

    // In your Svelte component

    // Define a function to fetch the JSON data
    async function fetchCredentials() {
        try {
            const response = await fetch(CREDENTIALS_URL);
            
            // Check if the response was successful
            if (response.ok) {
            credentials = await response.json();
            } else {
            console.error('Error:', response.status);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }

    // Call the function to fetch the credentials when needed
    onMount(fetchCredentials);


</script>


<!--Background for the header-->
<div style="position:fixed; background:white; left:0px; right:0px; top:0px; height:80px"></div>

<!--Clickable title in the header-->
<Button href='/' color=transparent style="position:fixed;right:30px;top:20px;">
    <Title 
    order={1} 
    variant='gradient' 
    gradient={{from: 'blue', to: 'red', deg: 45}} 
    style="font-size:40px; text-align:right; line-height:2">
        Sahlgrenska AI Hjälp
    </Title>
</Button>


<!--Burger menu-->
{#if opened}
<div class="burger-menu"> 
    <Stack override={{ height: 350 }}  align="center" spacing="xl">
        <Title order={2} variant='gradient' gradient={{from: 'blue', to: 'red', deg: 45}}>
            {credentials.username}
        </Title>
        <Button href='/chat' variant='gradient' gradient={{from: 'blue', to: 'red', deg: 45}} radius="lg" size="xl" ripple>
            Internethjälp
        </Button>
        <Button href='/' variant='gradient' gradient={{from: 'blue', to: 'red', deg: 45}} radius="lg" size="xl" ripple>
            Logga ut
        </Button>
    </Stack>
</div>
{/if}


<!--Burger button-->
<div style="position:fixed; left:30px; top:20px">
    <Burger color="blue"
    {opened}
    on:click={() => (opened = !opened)}
    />
</div>  


<!--Conversation-->
<div class="center-screen">
    <Conversation bind:check_for_messages={update_conversation}></Conversation>
</div>


<!--Input area-->
<div class="gradient-strip-bottom">
    <Center style="padding:20px">  
        <Group spacing="lg" direction="row">
                <form autocomplete="off" on:submit|preventDefault={handleSubmit}>
                    <Center>
                        <Group spacing="lg" direction="row">
                            <Input 
                                name="prompt"
                                variant="filled"
                                placeholder="T.ex 'Jag har feber och ont i huvudet, vad borde jag göra?'"
                                radius="lg"
                                size="l"
                                style="width:20cm"
                            />
                            <Button type="submit" color='teal' ripple>Skicka</Button>
                        </Group>
                    </Center>
                </form>
        </Group>
    </Center>
</div>





<style>
    .center-screen {
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    min-height: 100vh;
    }

    .gradient-strip-bottom {
    background: rgb(34,193,195);
    background: linear-gradient(45deg, rgba(34,193,195,1) 0%, rgba(0,80,200,1) 50%, rgba(34,193,195,1) 100%);
    position: fixed; 
    bottom: 0; 
    left: 0; 
    right: 0; 
    height: 80px;
    }

    .burger-menu {
    background: white;
    /*background: rgb(34,193,195);*/
    /*background: linear-gradient(45deg, rgba(34,193,195,1) 0%, rgba(0,80,200,1) 50%, rgba(34,193,195,1) 100%);*/
    position: fixed; 
    top: 100px; 
    left: 0;  
    bottom: 100px;
    width: 200px;
    }


</style>