<script>
    import { Text, Stack, Group, Title } from '@svelteuidev/core';
</script>



<div class="center-screen">
    <Group spacing="lg" direction="column">
        <Title order={1} variant='gradient' gradient={{from: 'blue', to: 'red', deg: 45}} style="font-size: 5rem">
            MedHelp
        </Title>

        <Stack override={{ height: 300 }}  align="flex-start" spacing="lg">
            <Text
                component='span'
                align='center'
                variant='gradient'
                size='xl'
                weight='bold'
            >
                Text with gradient
            </Text>

            <Text
            component='span'
            align='center'
            variant='gradient'
            size='xl'
            weight='bold'
        >
            Text with gradient
        </Text>

        </Stack>

    </Group>
    <Text
    component='span'
    align='center'
    variant='gradient'
    size='xl'
    weight='bold'
    gradient={{ from: 'red', to: 'yellow' }} 
>
    Text with gradient
</Text>
</div>

