<script>
    import { Button, Center, Stack, Text, Flex, Paper, SimpleGrid, RadioGroup, Switch, Space } from '@svelteuidev/core';
    import { onMount } from 'svelte';
    import { scale, slide } from 'svelte/transition';
    import { ChevronDown, ChevronUp } from 'radix-icons-svelte';

    let show_settings = false;

    //Language settings
    let language_value = 'normal';

    const language_options = [
        { label: 'Enkelt', value: 'easy' },
        { label: 'Vardagligt', value: 'normal' },
        { label: 'Medicinskt', value: 'complex' }
    ];


    //Tool settings
    let tool_options = [
        { label: '1177.se', checked: true },
        { label: 'FASS.se', checked: true },
        { label: 'internetmedicin.se', checked: true }
    ];



    const CLEAN_CONTEXT = {
        'chat_type': 'internet',
        'settings': {},
        //...
    };

    let context = {...CLEAN_CONTEXT};

    // Runs on page load and when settings are applied
    async function updateContext() {

        let chat_type = await fetch("http://localhost:5001/context");
        chat_type = await chat_type.json();
        chat_type = chat_type['chat_type'];

        if (chat_type == 'internet'){
            let chosen_tools = [];
            
            for (const tool of tool_options) {
                if (tool['checked'] == true) {
                    chosen_tools.push(tool['label'])
                }
            };

            context['settings'] = {
                'language_level': language_value,
                'chosen_tools': chosen_tools
            };
        }

        context['chat_type'] = chat_type

        const response = await fetch("http://localhost:5001/context", {
            method: "PUT",
            body: JSON.stringify(context),
            headers: {"Content-type": "application/json; charset=UTF-8"}
        });

        context = await response.json();
    }
    
    /*async function fetchContext() {
        const response = await fetch("http://localhost:5001/context");

        context = await response.json();
    }*/

    onMount(updateContext);

</script>


<!--Settings menu-->
<Center>
    <div class="settings">
        <Center>
            <Flex override={{ gap: 0 }} direction="column" align="center">
                
                <!--Settings content-->
                {#if show_settings == true}
                <div class="settings-window" in:scale={{delay:0}}>
                    <Paper shadow="xl" override={{ paddingLeft: 20, paddingRight: 20, paddingTop: 0 }}>
                        <Stack>

                            <!--Close settings button-->
                            <Center>
                                <Button on:click={() => (show_settings = !show_settings)} color="white" size="xl" compact ripple>
                                    <Flex justify="center" direction="column" override={{ gap: 0 }}>
                                        <Center><ChevronDown color="black"/></Center>
                                        <Center>
                                            <Text size='sm' variant='gradient' gradient={{from: 'blue', to: 'red', deg: 45}} style="line-height:1.5">
                                                Inställningar
                                            </Text>
                                        </Center>
                                    </Flex>
                                </Button>
                            </Center>

                            <!-- Individual settings -->
                            <SimpleGrid  cols={2}>

                                <!-- Language level settings -->
                                <div>
                                    <Stack>
                                        <Text size='md' variant='gradient' gradient={{from: 'blue', to: 'red', deg: 45}} style="line-height:1.5">Språknivå</Text>
    
                                        <Text size='xs' variant='gradient' gradient={{from: 'blue', to: 'red', deg: 45}} style="line-height:1.5">
                                            <RadioGroup bind:value={language_value} items={language_options} color='orange' size='sm' direction='column' spacing='xs' labelDirection='left'/>
                                        </Text>
                                    </Stack>
                                </div>


                                <!-- Internet tool setting -->
                                {#if context['chat_type'] == 'internet'}
                                <div>
                                    <Stack>
                                        <Text size='md' variant='gradient' gradient={{from: 'blue', to: 'red', deg: 45}} style="line-height:1.5">Källor</Text>
                                        
                                        <Text size='xs' variant='gradient' gradient={{from: 'blue', to: 'red', deg: 45}} style="line-height:1.5">
                                            <Stack spacing="xs">
                                                {#each tool_options as {label,checked}}
                                                <Switch {checked} 
                                                    on:change={() => checked = !checked}
                                                    label={label}
                                                    color="orange"
                                                />
                                                {/each}
                                            </Stack>
                                        </Text>
                                    </Stack>
                                </div>
                                {/if}
    
                                <!-- To add more settings, add a div with whatever buttons we want -->
                                


                            </SimpleGrid>

                            <!-- Apply settings button -->
                            <div>
                                <Flex justify="right">
                                    <!-- Behövs bara ifall det faktiskt stämmer
                                    <Center>
                                        <Text size='xs' variant='gradient' gradient={{from: 'blue', to: 'red', deg: 45}} style="line-height:1.5">*När du tillämpar nollställs botens minne*</Text>
                                    </Center>
                                    <Space w={20} ></Space> -->
                                    <Button on:click={updateContext} variant='subtle' color='orange' ripple>Tillämpa</Button>
                                </Flex>
                                
                            </div>
                        </Stack>
                        
                    </Paper>
                </div>

                {:else}

                <!--Open settings button-->
                <Button on:click={() => (show_settings = !show_settings)} color="white" size="xl" compact ripple>
                    <Flex justify="center" direction="column" override={{ gap: 0 }}>
                        <Center><ChevronUp color="black"/></Center>
                        <Center>
                            <Text size='sm' variant='gradient' gradient={{from: 'blue', to: 'red', deg: 45}} style="line-height:1.5">
                                Inställningar
                            </Text>
                        </Center>
                    </Flex>
                </Button>

                {/if}

            </Flex>
        </Center>
    </div>
</Center>




<style>

    .settings {
        background: transparent; 
        position: absolute; 
        margin: 85px; 
        bottom: 0; 
        height: fit-content; 
        width: 600px;
    }

    .settings-window {
        max-height: 80vh;
        height: fit-content;
        width: 600px;
    }

</style>