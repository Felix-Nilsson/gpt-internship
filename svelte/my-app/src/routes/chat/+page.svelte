<script>
    import { Group, Title, Input , Button, Center, Burger, Stack, Text, Paper, Divider, ActionIcon, Flex } from '@svelteuidev/core';
    import { scale, slide } from 'svelte/transition';
    import Conversation from "./Conversation.svelte";
    import Settings from "./Settings.svelte";
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation'
    import { Trash } from 'radix-icons-svelte';

    let current_chat = [] // messages of the current chat
    let all_chats = [[{'content': 'blablbalbabla'}], [{'content': 'bloloblblboblonsdjgdsglsjlgsglbslgsbligsfilgl'}]] // array containing all chats

    let opened = true;
    let input = "";

    let current_credentials = {
            'success': false,
            'login_as': 'None',
            'username': 'None'
        };

    let settings = {};

    //Backend should be running on port 5001
    const DATA_URL = 'http://localhost:5001/chat';

    const CREDENTIALS_URL = 'http://localhost:5001/credentials'

    let get_response;
    let update_conversation;

    
    const handleSubmit = async (e) => {

        //data contains the input
        let data = new FormData(e.target);
        
        //Clear input
        input = '';
        
        await get_response(data.get('prompt'), settings);
	}

    // Ensure that the user has logged in
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

    async function logout() {
        // Logout
        await fetch(CREDENTIALS_URL, {
            method: "DELETE",
        });
        goto("/");
    }

    async function clear_backend() {
        await fetch(DATA_URL, {method: "DELETE"});
        await update_conversation();
    }

    // Call the function to fetch the credentials when needed
    onMount(fetchCredentials, clear_backend, setup_chat);

    const CHATS_URL = 'http://localhost:5001/all-chats';

    async function setup_chat() {
        const response = await fetch(CHATS_URL, {
            method: "GET"
        });
        const data = await response.json();
        all_chats = data;
    }

    async function new_chat() {
        const response = await fetch(CHATS_URL, {
            method: "POST"
        });
        const data = await response.json();
        all_chats = data;
    }


    async function change_current_chat(chat_index) {
        const response = await fetch(CHATS_URL, {
            method: "PUT",
            body: JSON.stringify({'new_id': chat_index}),
            headers: {"Content-type": "application/json; charset=UTF-8"}
        });
        const data = await response.json();
        all_chats = data;
    }

    async function delete_chat(chat_index) {
        const response = await fetch(CHATS_URL, {
            method: "PATCH",
            body: JSON.stringify({'delete_id': chat_index}),
            headers: {"Content-type": "application/json; charset=UTF-8"}
        });
        const data = await response.json();
        all_chats = data;
    }


</script>


<!--Conversation-->
<Conversation bind:messages={current_chat} bind:get_response={get_response} bind:get_conversation={update_conversation}></Conversation>


<!--Burger menu-->
{#if opened}
<div class="burger-menu" transition:slide={{ duration: 350, axis: 'x' }}> 

    <div style="position:absolute; top:0; right:0; height:100vh">
        <Divider orientation='vertical'/>
    </div>

    <Stack align="center" spacing="md">

        <Button fullSize on:click={new_chat} variant='gradient' gradient={{from: 'teal', to: 'blue', deg: 45}} ripple>Ny Chat</Button>
        
        <div style="height: calc(100vh - 260px); overflow: auto;">
        <!-- TODO ADD CHATS -->
        {#each all_chats as chat, i}
        <Flex gap={0} style="align: center;">
            <Button on:click={() => change_current_chat(i)} 
                size={40} 
                fullSize 
                variant='subtle'
                color='cyan'
                style="max-width: 160px; overflow: hidden; align-items: left;"
                ripple>
                {#if chat.length > 0}
                {String(chat[0]['content']).slice(0, 15) + '...'}
                {/if}
            </Button>
            
            <ActionIcon on:click={() => delete_chat(i)} color='red' size={40}>
                <Trash/>
            </ActionIcon>
        </Flex>
        {/each}
        </div>


        {#if current_credentials['success']}
            <!-- Logout button -->
            <div style="position: absolute; bottom: 40px">
                <Button type="button" on:click={logout} variant='outline' color='cyan' ripple>
                    Logga ut
                </Button>
            </div>
        {/if}
        

        <!-- TODO This should probably be removed at some point, as it is just for convenience when testing     -->
        <div style="position: absolute; bottom: 5px">
            <Button type="button" on:click={update_conversation} variant='subtle' color='cyan' size='xs' ripple>uppdatera</Button>
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


<!--Settings-->
<Settings bind:settings={settings} bind:login_as={current_credentials['login_as']}></Settings>



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
            {#if current_credentials["login_as"] == "patient"}
                Patientassistent
            {:else if current_credentials["login_as"] == "doctor"}
                Läkarassistent
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
                Medicinsk AI-Hjälp 
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
        right: 90px;
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
        z-index: 11;
    }

    .burger-menu {
        background: white;
        position: fixed; 
        top: 80px; 
        padding: 20px;
        left: 0;  
        bottom: 0px;
        width: 200px;
        overflow: hidden;
        z-index: 12;
    }



</style>