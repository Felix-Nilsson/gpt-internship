<script>
    import { Button, Group, Title } from '@svelteuidev/core';
    import { goto } from '$app/navigation'


    async function set_assistant(type) {

        console.log("Routing to chat: " + type)

        goto("/login?login_as=" + type);
    }

</script>

<svelte:head>
    <title>Medicinsk AI-Hjälp</title> 
</svelte:head>


<div class="center-screen">
    <Group spacing="lg" direction="column">
        <!--Title-->
        <Title order={1} variant='gradient' gradient={{from: 'blue', to: 'red', deg: 45}} style="font-size: 5rem; line-height: 1.5">
            Medicinsk AI-Hjälp
        </Title>
        <!--Patient help button-->
        <Button on:click={() => set_assistant("patient")} variant='gradient' gradient={{from: 'teal', to: 'blue', deg: 60}} radius="lg" size="xl" ripple>
            Patientassistent
        </Button>
        <!--Doctor assistant button-->
        <Button on:click={() => set_assistant("doctor")} variant='gradient' gradient={{from: 'teal', to: 'blue', deg: 60}} radius="lg" size="xl" ripple>
            Läkarassistent
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