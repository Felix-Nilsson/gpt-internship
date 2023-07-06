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
    <ThemeIcon variant='gradient' gradient={{from: 'teal', to: 'blue', deg: 45}} size="xl" radius="lg">
        <Icon icon="radix-icons:person" />
    </ThemeIcon>

    <Paper shadow="xl" radius="lg">
        <Title order={3} variant='gradient' gradient={{from: 'blue', to: 'teal', deg: 45}} align="left" style="word-wrap;break-word;">
            <div bind:this={thisObj}>
                <slot/>
            </div>
        </Title>
    </Paper>
</Group>

