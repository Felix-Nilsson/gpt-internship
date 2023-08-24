<script>
    import { Group, Title, Input , Button, Center, Burger, Stack, Text, Paper, Divider, ActionIcon, Flex } from '@svelteuidev/core';
    import { scale, slide } from 'svelte/transition';
    import Conversation from "./Conversation.svelte";
    import Settings from "./Settings.svelte";
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation'
    import { Trash } from 'radix-icons-svelte';

    // ID of the current chat
    let chat_id = 0;
    // Array with a 'title' for each chat (it's the first user query for that chat)
    let chats_titles = [];
    let can_create_new_chat = false;

    let opened = true;
    let input = "";

    let current_credentials = {
            'success': false,
            'login_as': 'None',
            'username': 'None'
        };

    let settings = {};

    // Backend adresses
    const CREDENTIALS_URL = 'http://localhost:5001/credentials'
    const CHATS_URL = 'http://localhost:5001/all-chats';

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

    onMount(fetchCredentials);

    async function logout() {
        // Logout
        await fetch(CREDENTIALS_URL, {
            method: "DELETE",
        });
        goto("/");
    }

    

    async function setup_chats() {
        const response = await fetch(CHATS_URL, {
            method: "GET"
        });
        const data = await response.json();
        chats_titles = data;

        await update_conversation();
        await check_if_can_create_new_chat(chats_titles)
    }

    // Setup the chats on page load
    onMount(setup_chats);

    async function new_chat() {
        const response = await fetch(CHATS_URL, {
            method: "POST"
        });
        const data = await response.json();
        chat_id = 0;
        chats_titles = data;

        await update_conversation();
        await check_if_can_create_new_chat(chats_titles)
    }


    async function change_current_chat(chat_index) {
        chat_id = chat_index
        const response = await fetch(CHATS_URL, {
            method: "PUT",
            body: JSON.stringify({'new_id': chat_index}),
            headers: {"Content-type": "application/json; charset=UTF-8"}
        });
        const data = await response.json();
        chats_titles = data;

        await update_conversation();
        await check_if_can_create_new_chat(chats_titles)
    }

    async function delete_chat(chat_index) {
        const response = await fetch(CHATS_URL, {
            method: "PATCH",
            body: JSON.stringify({'delete_id': chat_index}),
            headers: {"Content-type": "application/json; charset=UTF-8"}
        });
        const data = await response.json();
        chats_titles = data;

        await update_conversation();
        await check_if_can_create_new_chat(chats_titles)
    }

    async function event_update_chats(event) {
        console.log('Event, updating chats')
        const response = await fetch(CHATS_URL, {
            method: "GET"
        });
        const data = await response.json();

        await check_if_can_create_new_chat(data)

        // Trigger a reload of the chat history pane
        chats_titles = data
    }

    async function check_if_can_create_new_chat(chats_titles) {
        can_create_new_chat = true
        chats_titles.forEach(title => {
            if (title == '') {
                // Title is empty -> empty chat -> do not let user create new chat
                can_create_new_chat = false                
            }
        });
    }

</script>


<!--Conversation-->
<Conversation on:update={event_update_chats} bind:get_response={get_response} bind:get_conversation={update_conversation}/>


<!--Burger menu-->
{#if opened}
<div class="burger-menu" transition:slide={{ duration: 350, axis: 'x' }}> 

    <div style="position:absolute; top:0; right:0; height:100vh">
        <Divider orientation='vertical'/>
    </div>

    <Stack align="center" spacing="md">

        <Button fullSize on:click={new_chat} variant='gradient' gradient={{from: 'teal', to: 'blue', deg: 45}} disabled={!can_create_new_chat} ripple>Ny Chat</Button>
        
        <div style="height: calc(100vh - 260px); overflow: auto;">
        <!-- TODO ADD CHATS -->
        {#if chats_titles.length != 0}
            {#each chats_titles as title, i}
            <Flex gap={0} style="align: center;">
                {#if i == chat_id}
                <Button on:click={() => change_current_chat(i)} 
                    size={40} 
                    variant='outline'
                    color='cyan'
                    style="width: 160px; padding: 5px; overflow: hidden; justify-content:left"
                    ripple>
                    {#if title == ''}
                        (ny chat)
                    {:else if title.length > 18}
                        {String(title).slice(0, 15) + '...'}
                    {:else}
                        {title}
                    {/if}
                </Button>
                {:else}
                <Button on:click={() => change_current_chat(i)} 
                    size={40} 
                    variant='subtle'
                    color='cyan'
                    style="width: 160px; padding: 5px; overflow: hidden; justify-content:left"
                    ripple>
                    {#if title == ''}
                        (ny chat)
                    {:else if title.length > 18}
                        {String(title).slice(0, 15) + '...'}
                    {:else}
                        {title}
                    {/if}
                </Button>
                {/if}
                
                

                <ActionIcon on:click={() => delete_chat(i)} color='red' size={40}>
                    <Trash/>
                </ActionIcon>
            </Flex>
            {/each}
        {/if}
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
                                style="width: calc(100vw - 680px);box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.07); border-radius: 8px;"
                            />
                            <Button color="teal" ripple>Skicka</Button>
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
        <ActionIcon size={60}
       
            on:click={() => (opened = !opened)}
        >
            <Burger color="black" 
            {opened}
           
            
            />
        </ActionIcon>
        
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
        top: 10px;
    }

    .burger-button:hover {
        background-color: #d2d2d2;
        border-radius: 5px;
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
        /* background: rgb(34,193,195);
        background: linear-gradient(45deg, rgba(34,193,195,1) 0%, rgba(0,80,200,1) 50%, rgba(34,193,195,1) 100%);*/
        background: transparent;
        position: fixed; 
        bottom: 0; 
        left: 0; 
        right: 0; 
        height: 80px;
        z-index: 11;
    }

    .burger-menu {
        background: #ffffff;
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