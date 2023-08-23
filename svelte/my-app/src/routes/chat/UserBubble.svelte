<script>
    import { onMount } from 'svelte';
    import { Flex, Text, Paper, ThemeIcon } from '@svelteuidev/core';
    import Icon from '@iconify/svelte';

    let thisObj;
    let message = '';

    onMount(() => {
        message = thisObj.textContent;
    })

</script>

<Flex gap="lg">
    <Paper shadow="xl" radius="lg" style="max-width: 55vw; background: rgb(18,183,135);
    background: linear-gradient(45deg, rgba(18,183,135,1) 0%, rgba(34,140,229,1) 100%);">
        <Text 
        color="white"
        align="left" 
        size='lg'
        weight='normal'
        style="word-wrap: break-word; line-height: 1.5;">
            <div bind:this={thisObj}>
                <slot />
            </div>
        </Text>
    </Paper>

    <ThemeIcon variant='gradient' gradient={{from: 'blue', to: 'teal', deg: 45}} size="xl" radius="lg">
        <Icon icon="radix-icons:person" />
    </ThemeIcon>
</Flex>

