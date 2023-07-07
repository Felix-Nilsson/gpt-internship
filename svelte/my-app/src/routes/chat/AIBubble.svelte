<script>
    import { onMount } from 'svelte';
    import { Flex, Group, Title, Paper, ThemeIcon,
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

<Flex justify="right" gap="lg">
    <Paper shadow="xl" radius="lg" style="max-width: 55vw">
        <Title order={3} variant='gradient' gradient={{from: 'red', to: 'yellow', deg: 45}} align="right" style="word-wrap: break-word;">
            <div bind:this={thisObj}>
                <slot />
            </div>
        </Title>
    </Paper>

    <ThemeIcon variant='gradient' gradient={{from: 'yellow', to: 'red', deg: 45}} size="xl" radius="lg">
        <Icon icon="carbon:bot"/>
    </ThemeIcon>
</Flex>



