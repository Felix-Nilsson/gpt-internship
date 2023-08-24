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

<!-- gradient={{from: 'blue', to: 'teal', deg: 45}} -->

<Flex justify="right" gap="lg">
    <ThemeIcon variant='outline' size="xl" radius="lg" style="linear-gradient(45deg, rgba(18,183,135,1) 0%, rgba(34,140,229,1) 100%);">
        <Icon icon="carbon:bot" />
    </ThemeIcon>
    
    <Paper shadow="xl" radius="lg" style="max-width: 55vw">
        <Text 
        variant='gradient' 
        gradient={{from: 'blue', to: 'teal', deg: 45}} 
        align="left" 
        size='lg'
        weight='normal'
        style="white-space: pre-line; word-wrap: break-word; line-height: 1.5;">
            <div bind:this={thisObj}>
                <slot />
            </div>
        </Text>
    </Paper>
</Flex>



