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

<Flex justify="right" gap="lg">
    <Paper shadow="xl" radius="lg" style="max-width: 55vw">
        <Text 
        variant='gradient' 
        gradient={{from: 'red', to: 'yellow', deg: 45}} 
        align="left" 
        size='lg'
        weight='normal'
        style="word-wrap: break-word; line-height: 1.5;">
            <div bind:this={thisObj}>
                <slot />
            </div>
        </Text>
    </Paper>

    <ThemeIcon variant='gradient' gradient={{from: 'yellow', to: 'red', deg: 45}} size="xl" radius="lg">
        <Icon icon="carbon:bot"/>
    </ThemeIcon>
</Flex>



