<script>
    import { Group, Title, Input , Button, Center, Burger, Stack, Text, Space, Divider } from '@svelteuidev/core';
    import Conversation from "./Conversation.svelte";
    import Settings from "./Settings.svelte";
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation'

    let opened = false;
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
        clear_backend();
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
    onMount(fetchCredentials, clear_backend);

</script>


<!--Conversation-->
<Conversation bind:get_response={get_response} bind:get_conversation={update_conversation}></Conversation>


<!--Burger menu-->
{#if opened}
<div class="burger-menu"> 

    <div style="position:absolute; top:0; right:0; height:100vh">
        <Divider orientation='vertical'/>
    </div>

    <Stack align="center" spacing="lg">

        <Space h={20}/>

        <div style="width: 160px;">
            <Text size='xs' align='left' variant='gradient' gradient={{from: 'blue', to: 'red', deg: 45}} style="line-height:1.5">
                <h1>{(current_credentials['success'] == true) ? 'Välkommen,' : ' '}</h1>
                <h3>{(current_credentials['success'] == true) ? current_credentials['username'] : ' '}</h3>

                <h2 id="about">Om</h2>
                <p>Ett första försök att bygga en chatt-bot för läkare och patienter med GPT modeller, gjort i sammarbete mellan AI-Sweden och Sahlgrenska Universitetssjukhus under GPT Summer Internship 2023.</p>
                <p>Skapat av:</p>
                <ul>
                    <li>Henrik Johansson</li>
                    <li>Oskar Pauli</li>
                    <li>Felix Nilsson</li>
                </ul>
                <p>🔗 <a href="https://my.ai.se/projects/287">Projektsida</a></p>
                <p>📝 Note: Ingen av den patientdata som används är äkta, allt har generats specifikt för detta projektet.</p>
            </Text>
        </div>



        <!--<div style="position: absolute; bottom: 110px">
            <Button on:click={goto_internet} variant='gradient' gradient={{from: 'blue', to: 'red', deg: 45}} ripple disabled={(current_credentials['login'] == 'internet') ? true : false}>
                Internetassistent
            </Button>
        </div>-->
        
        {#if current_credentials['success']}
            <!-- Logout button -->
            <div style="position: absolute; bottom: 50px">
                <Button type="button" on:click={logout} variant='outline' color='cyan' ripple>
                    Logga ut
                </Button>
            </div>
        {/if}
        

        <!-- TODO TODO TODO TODO      Probably remove this, as it is just for convenience when testing     -->
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