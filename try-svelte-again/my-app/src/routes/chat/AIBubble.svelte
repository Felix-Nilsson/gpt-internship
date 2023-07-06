<script>
    import { onMount } from 'svelte';
    import { Group, Title, Paper, ThemeIcon,
         Input , Button, Center, Burger, Navbar, Header,} from '@svelteuidev/core';
    import { typewriter } from '@svelteuidev/motion';
    import Icon from '@iconify/svelte';

    let thisObj;
    let message = '';

    onMount(() => {
        message = thisObj.textContent;
    })
    console.log(message)

</script>

<Group spacing="lg" direction="row">
    <Paper shadow="xl" radius="lg">
        <Title order={3} variant='gradient' gradient={{from: 'red', to: 'yellow', deg: 45}} align="left">
            <div bind:this={thisObj}>
                <slot />
            </div>
        </Title>
    </Paper>

    <ThemeIcon variant='gradient' gradient={{from: 'yellow', to: 'red', deg: 45}} size="xl" radius="lg">
        <Icon icon="carbon:bot"/>
    </ThemeIcon>
</Group>



