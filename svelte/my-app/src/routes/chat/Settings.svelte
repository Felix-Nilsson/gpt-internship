<script>
    import { Button, Center, Stack, Text, Flex, Paper, SimpleGrid, RadioGroup, Switch, Space, Divider, ActionIcon } from '@svelteuidev/core';
    import { onMount, tick } from 'svelte';
    import { scale, slide } from 'svelte/transition';
    import { Gear } from 'radix-icons-svelte';

    export let login_as = ''; // Set this from parent
    export let settings = {}; // Bind to this so parent can access it
    
    // Change this to false if we do not want settings to be open by default
    let show_settings = true;

    //Chatbot choice
    let chatbot_value;
    let chatbot_options;

    const patient_options = [
        { label: 'Patientassistent', value: 'patient' },
        { label: 'Internetassistent', value: 'internet' }
    ];
    
    const doctor_options = [
        { label: 'Läkarassistent', value: 'doctor' },
        { label: 'Intranätassistent', value: 'intranet' },
        { label: 'Internetassistent', value: 'internet' }
    ];

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


    // Runs on page load and when settings are applied
    function updateSettings() {

        // Setup chatbot setting
        if (chatbot_value == null) {
            if (login_as == 'patient') {
                chatbot_value = 'patient';
                chatbot_options = patient_options;
            } else if (login_as == 'doctor') {
                chatbot_value = 'doctor';
                chatbot_options = doctor_options;
            }
        }
        

        let chosen_tools = [];
        
        for (const tool of tool_options) {
            if (tool['checked'] == true) {
                chosen_tools.push(tool['label'])
            }
        };

        settings['language_level'] = language_value;
        settings['chosen_tools'] = chosen_tools;
        settings['chatbot_type'] = chatbot_value;
    }

    const timer = ms => new Promise(res => setTimeout(res,ms))

    // IF WE DO NOT WAIT BEFORE UPDATING SETTINGS ON MOUNT WE LOOSE IMPORTANT INFO
    onMount(() => setupSettings(500))
    const setupSettings = async (ms) => {
        await timer(ms); 
        
        updateSettings()
    }

    function settings_button() {
        updateSettings()

        show_settings = !show_settings
    }

</script>

<!-- SETTINGS BUTTON -->
<div class="settings-button">
    <ActionIcon variant='transparent' size={40} color='red' on:click={settings_button}>
        <Gear size={35}/>
    </ActionIcon>
</div>


<!-- SETTINGS PANEL -->
{#if show_settings}
<div class="settings-menu"> 

    <div style="position:absolute; top:0; left:0; bottom:80px; height:100vh">
        <Divider orientation='vertical'/>
    </div>

    <Stack align="center" spacing="lg">

        <Space h={20}/>

        <div style="width: 160px;">
            <Text size='xs' align='left' variant='gradient' gradient={{from: 'blue', to: 'red', deg: 45}} style="line-height:1.5">
                Inställningar
            </Text>
        </div>

        <!-- Individual settings -->
        <SimpleGrid  cols={1}>

            <!-- Chatbot choice -->
            <div>
                <Stack>
                    <Text size='md' variant='gradient' gradient={{from: 'blue', to: 'red', deg: 45}} style="line-height:1.5">Val av chat</Text>

                    <Text size='xs' variant='gradient' gradient={{from: 'blue', to: 'red', deg: 45}} style="line-height:1.5">
                        <RadioGroup bind:value={chatbot_value} items={chatbot_options} color='orange' size='sm' direction='column' spacing='xs' labelDirection='left'/>
                    </Text>
                </Stack>
            </div>


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
            <div>
                <Stack>
                    <Text size='md' variant='gradient' gradient={{from: 'blue', to: 'red', deg: 45}} style="line-height:1.5">Källor (internet)</Text>
                    
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
                <Button on:click={updateSettings} variant='subtle' color='orange' ripple>Tillämpa</Button>
            </Flex>
            
        </div>


    </Stack>
</div>
{/if}


<style>

    .settings-button {
        position: fixed;
        right: 30px;
        top: 20px;
        z-index: 10;
    }

    .settings-menu {
        background: white;
        position: fixed; 
        top: 80px; 
        right: 0;  
        bottom: 80px;
        width: 200px;
    }

</style>