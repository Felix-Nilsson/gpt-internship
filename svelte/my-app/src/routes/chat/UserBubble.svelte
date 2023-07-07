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

<Flex gap="lg">
    <ThemeIcon variant='gradient' gradient={{from: 'teal', to: 'blue', deg: 45}} size="xl" radius="lg">
        <Icon icon="radix-icons:person" />
    </ThemeIcon>

    <Paper shadow="xl" radius="lg" style="max-width: 55vw">
        <Title 
        order={3} 
        variant='gradient' 
        gradient={{from: 'blue', to: 'teal', deg: 45}} 
        align="left" 
        style="word-wrap: break-word; line-height: 1.5;">
            <div bind:this={thisObj}>
                <slot/>
            </div>
        </Title>
    </Paper>
</Flex>

