<script>
    import { Group, Title, Paper, ThemeIcon,
         Input , Button, Center, Burger, Navbar, Header, Stack, Divider} from '@svelteuidev/core';
    import Icon from '@iconify/svelte';
    import Conversation from "./Conversation.svelte";

    let opened = false;
    let input = "";

    //Backend should be running on port 5001
    const DATA_URL = 'http://localhost:5001/data';

    let update_conversation;

    const handleSubmit = async (e) => {

        //data contains the input
        let data = new FormData(e.target);

        //Clear input
        input = '';

        //Send a update request. The backend will generate a response and update the conversation.
        await fetch(DATA_URL, {
            method: "PUT",
            body: JSON.stringify({'prompt': data.get('prompt')}),
            headers: {"Content-type": "application/json; charset=UTF-8"}
        });

		//Start looking for a response
		await update_conversation();
	}

    async function clear_backend() {
        await fetch('http://localhost:5001/data/get', {method: "DELETE"});
        await update_conversation(1, true);
    }


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
            Sven Svensson
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
                            <Button type="button" on:click={clear_backend} variant='gradient' gradient={{from: 'teal', to: 'blue', deg: 45}} ripple>Ny Chat</Button>
                            <Input 
                                name="prompt"
                                bind:value={input}
                                variant="filled"
                                placeholder="T.ex 'Jag har feber och ont i huvudet, vad borde jag göra?'"
                                radius="lg"
                                size="l"
                                style="width:20cm"
                            />
                            <Button type="submit" variant='gradient' gradient={{from: 'yellow', to: 'orange', deg: 45}} ripple>Skicka</Button>
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