<script>
    import { Input, Space, Title, Group, Button, Stack, Text } from '@svelteuidev/core';
    import { LockClosed, Person } from 'radix-icons-svelte';
    import { goto } from '$app/navigation'
    import { onMount } from 'svelte';
    
    
    const timer = ms => new Promise(res => setTimeout(res,ms))
    let login_result = false;
    
    let type = '';
    
    let login_invalid = false;

    function get_type_from_url_params() {
        const urlParams = new URLSearchParams(window.location.search)
        type = urlParams.get('login_as')
    }

    onMount(get_type_from_url_params)

    const handleSubmit = async (e) => {
        login_invalid = false;

        //get the input from the fields
        let input = new FormData(e.target);

        const response = await fetch("http://localhost:5001/credentials", {
            mode:"cors",
            method: "PUT",
            body: JSON.stringify({'username': input.get("usernamefield"), "password": input.get("passwordfield"), "login_as": type}),
            headers: {"Content-type": "application/json; charset=UTF-8"}
        });

        const data = await response.json();

        let result = data['success'];
        login_result = result;

        if (login_result == true){
            console.log("Login successful")
            console.log(input.get("usernamefield") + " " + input.get("passwordfield"))
            goto("/chat");
        } else {
            login_invalid = true;
            console.log("Wrong username/password")
        }
        
    }

</script>
  

<div class="center-screen">
    <Group spacing="lg" direction="column">

        <Button href='/' color=white>
            <Title order={1} variant='gradient' gradient={{from: 'blue', to: 'red', deg: 45}} style="font-size: 5rem; line-height: 1.5">
                Medicinsk AI-Hjälp
            </Title>
        </Button>
        <Space h=lg/>
        <Title
                order={2} 
                style="font-size: 2rem; line-height: 1.5"
                weight="thin"
                color="gray"
                >
                    Välkommen! Du loggar in som {#if type == "doctor"} läkare {:else} patient {/if}
        </Title>

       
    
        <form on:submit|preventDefault={handleSubmit}>
            <Stack spacing="lg">

                {#if login_invalid}
                <Text color="red">Fel användarnamn eller lösenord</Text>
                
                {/if}
                
                <Input 
                    icon={Person} 
                    placeholder="Användarnamn"
                    name="usernamefield"
                    radius="lg"
                    size="xl"
                    invalid={login_invalid}
                    
                />

                <Input 
                    type="password" 
                    icon={LockClosed} 
                    placeholder="Lösenord"
                    name="passwordfield"
                    radius="lg"
                    size="xl"
                    invalid={login_invalid}
                />

                
                <Button 
                    variant='gradient' 
                    gradient={{from: 'teal', to: 'blue', deg: 60}} 
                    radius="lg" size="lg" 
                    ripple 
                    type="submit"
                    fullSize
                >
                    Skicka
                </Button>
                <Text 
                    on:click={() => goto("/")} 
                    color='grey' 
                    underline 
                    align="center" 
                    style="cursor:pointer; line-height: 1.5;"
                >
                    
                    Tillbaka till hemskärmen
                    
                </Text>

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