<script>
    import { Button, Group, Title } from '@svelteuidev/core';
    import { goto } from '$app/navigation'


    async function set_assistant(type) {

        console.log("setting assistant type to " + type + " and resetting any ongoing chats")

        await fetch("http://localhost:5001/settings", {
            method: "PUT",
            body: JSON.stringify({'type': type}),
            headers: {"Content-type": "application/json; charset=UTF-8"}
        });
        
        if (type == "internet"){
            goto("/chat")
        } else {
            goto("/login")
        }
            
    }





</script>


<div class="center-screen">
    <Group spacing="lg" direction="column">
        <!--Title-->
        <Title order={1} variant='gradient' gradient={{from: 'blue', to: 'red', deg: 45}} style="font-size: 5rem; line-height: 1.5">
            Sahlgrenska AI Hjälp
        </Title>
        <!--Patient help button-->
        <Button on:click={() => set_assistant("patient")} variant='gradient' gradient={{from: 'teal', to: 'blue', deg: 60}} radius="lg" size="xl" ripple>
            Patientassistent
        </Button>
        <!--Doctor assistant button-->
        <Button on:click={() => set_assistant("doctor")} variant='gradient' gradient={{from: 'teal', to: 'blue', deg: 60}} radius="lg" size="xl" ripple>
            Läkarassistent
        </Button>

        <!--Intranet button-->
        <Button on:click={() => set_assistant("intranet")} variant='gradient' gradient={{from: 'teal', to: 'blue', deg: 60}} radius="lg" size="xl" ripple>
            Intranät
        </Button>
        <!--Internet button-->
        <Button on:click={() => set_assistant("internet")} variant='gradient' gradient={{from: 'teal', to: 'blue', deg: 60}} radius="lg" size="xl" ripple>
            Internet
        </Button>
    </Group>
</div>


<style>
    .center-screen {
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    min-height: 100vh;
    }
</style>