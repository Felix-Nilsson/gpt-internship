<script>
    import { Group, Title, Input , Button, Center, Burger, Stack, Text, Space, Divider } from '@svelteuidev/core';
    import Conversation from "./Conversation.svelte";
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation'


    let opened = false;
    let input = "";

    let current_credentials = {'username': ''};
    let context = {};

    //Backend should be running on port 5001
    const DATA_URL = 'http://localhost:5001/chat';

    const CREDENTIALS_URL = 'http://localhost:5001/credentials'

    let update_conversation;
    let new_message_load_animation;

    const handleSubmit = async (e) => {

        //data contains the input
        let data = new FormData(e.target);

        new_message_load_animation(data.get('prompt'));

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

        await fetchContext();
	}

    //We only have chat-type setting, but more will come
    async function fetchContext() {
        const response = await fetch("http://localhost:5001/context");

        context = await response.json();
    }

    onMount(fetchContext);


    //Attempt login
    async function fetchCredentials() {
        try {
            let response = await fetch(CREDENTIALS_URL);
            response = await response.json()
            
            // Check if the response was successful
            if (response['success']) {
                current_credentials = response;
            } 

        } catch (error) {
            console.error('Error:', error);
        }
    }

    // Call the function to fetch the credentials when needed
    onMount(fetchCredentials);

    async function logout() {
        await fetch(CREDENTIALS_URL, {
            method: "DELETE",
        });
        goto("/")
    }

    async function clear_backend() {
        await fetch(DATA_URL, {method: "DELETE"});
        await update_conversation();
        await fetchContext();
    }

    async function get_curr_conv() {
        await update_conversation();
    }

</script>


<!--Conversation-->
<Conversation bind:check_for_messages={update_conversation} bind:new_message_loading={new_message_load_animation}></Conversation>

<!--Burger menu-->
{#if opened}
<div class="burger-menu"> 

    <div style="position:absolute; top:0; right:0; height:100vh">
        <Divider orientation='vertical'/>
    </div>

    <Stack align="center" spacing="lg">

        <Text size='lg' variant='gradient' gradient={{from: 'blue', to: 'red', deg: 45}} style="text-align:center; line-height:1.5">
            {current_credentials['username']}
        </Text>

        <Space h={30}/>

        <Text size='lg' variant='gradient' gradient={{from: 'blue', to: 'red', deg: 45}} style="text-align:center; line-height:1.5">
            Testa de andra Chatterna:
        </Text>

        <!-- NEEDS A ONCLICK FUNCTION THAT SETS THE CORRECT CHAT -->
        <!-- IF WE EVEN WANT THESE, SURE IT DOES NOT MAKE SENSE TO MARKET THE DOCTOR ASSISTANT TO PATIENTS, etc... -->
        <!-- on:click={() => function("chat_type")} -->
        <Button href='/chat' variant='gradient' gradient={{from: 'blue', to: 'red', deg: 45}} ripple disabled={(context['chat_type'] == 'patient') ? true : false}>
            Patientassistent
        </Button>

        <Button href='/chat' variant='gradient' gradient={{from: 'blue', to: 'red', deg: 45}} ripple disabled={(context['chat_type'] == 'doctor') ? true : false}>
            Läkarassistent
        </Button>
        
        <Button href='/chat' variant='gradient' gradient={{from: 'blue', to: 'red', deg: 45}} ripple disabled={(context['chat_type'] == 'intranet') ? true : false}>
            Intranätassistent
        </Button>

        <Button href='/chat' variant='gradient' gradient={{from: 'blue', to: 'red', deg: 45}} ripple disabled={(context['chat_type'] == 'internet') ? true : false}>
            Internethjälp
        </Button>
        
        

        {#if current_credentials['success']}
            <!-- Username -->
            <div style="position: absolute; top: 50px">
                <Text size='lg' variant='gradient' gradient={{from: 'blue', to: 'red', deg: 45}} style="line-height:1.5">
                    {current_credentials['username']}
                </Text>
            </div>

            <!-- Logout button -->
            <div style="position: absolute; bottom: 50px">
                <Button type="button" on:click={logout} variant='outline' color='cyan' ripple>
                    Logga ut
                </Button>
            </div>
        {/if}
        

        <!-- TODO TODO TODO TODO      Probably remove this, as it is just for convenience when testing     -->
        <div style="position: absolute; bottom: 5px">
            <Button type="button" on:click={get_curr_conv} variant='subtle' color='cyan' size='xs' ripple>uppdatera</Button>
        </div>
    </Stack>
</div>
{/if}


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


<!--Header-->
<div class="header">

    <div style="position:absolute; bottom:0; left:0; width:100vw;">
        <Divider style="margin:0;"/>
    </div>

    <!--Burger button-->
    <div class="burger-button">
        <Burger color="blue"
        {opened}
        on:click={() => (opened = !opened)}
        />
    </div>

    <!--Chat-type indicator-->
    <div class="header-type">
        <Title
        style="
            font-size:30px; 
            text-align:left; 
            line-height:1.5"
        variant='gradient' 
        gradient={{from: 'blue', to: 'red', deg: 45}}
        order={1}>
            {#if context["chat_type"] == "patient"}
                Patientassistent
            {:else if context["chat_type"] == "doctor"}
                Läkarassistent
            {:else if context["chat_type"] == "intranet"}
                Intranät
            {:else}
                Internet
            {/if}
        </Title>
    </div>

    <!--Clickable title-->
    <div class="header-title">
        <Button href='/' color=transparent style="width:400px; height:50px">
            <Title 
            style="
                position:relative; 
                width:400px; 
                top:-5px; 
                font-size:40px; 
                text-align:right; 
                line-height:1.5"
            variant='gradient' 
            gradient={{from: 'blue', to: 'red', deg: 45}}
            order={1}>
                Sahlgrenska AI Hjälp 
            </Title>
        </Button>
    </div>
</div>







<style>
    
    .header {
        position: fixed;
        background: white;
        left: 0;
        right: 0;
        top: 0;
        height: 80px;
    }

    .burger-button {
        position: fixed;
        left: 30px;
        top: 20px;
    }

    .header-type {
        position: fixed;
        left: 90px;
        top: 12px;
    }

    .header-title {
        position: fixed;
        right: 30px;
        top: 15px;
        width: 400px;
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
        top: 80px; 
        left: 0;  
        bottom: 80px;
        width: 200px;
    }


</style>