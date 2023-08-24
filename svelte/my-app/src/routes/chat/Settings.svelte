<script>
    import { Stack, Text, SimpleGrid, RadioGroup, Switch, Divider, ActionIcon } from '@svelteuidev/core';
    import { onMount } from 'svelte';
    import { slide } from 'svelte/transition';
    import { Gear } from 'radix-icons-svelte';

    export let login_as = ''; // Set this from parent
    export let settings = {}; // Bind to this so parent can access it
    
    // Change this to false if we do not want settings to be open by default
    let show_settings = false;

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

    // Timer
    const timer = ms => new Promise(res => setTimeout(res,ms))

    // IF WE DO NOT WAIT BEFORE UPDATING SETTINGS ON MOUNT WE LOOSE IMPORTANT INFO
    onMount(async () => {
        await timer(500); 
        
        updateSettings()
    });
</script>

<!-- SETTINGS BUTTON -->
<div class="settings-button">
    <ActionIcon variant='transparent' size={60} color='black' on:click={() => {show_settings = !show_settings}}>
        <Gear size={35}/>
    </ActionIcon>
</div>


<!-- SETTINGS PANEL -->
{#if show_settings}
<div class="settings-menu" transition:slide={{ duration: 350, axis: 'x' }}>

    <div style="position:absolute; top:0; left:0; height:100vh">
        <Divider orientation='vertical'/>
    </div>

    <Stack align="center" spacing={0}>

        <div style="width: 160px;">
            <Text size='md' align='left' color="blue" style="line-height:1.5">
                <h3>Inställningar</h3>
            </Text>
        </div>

        <!-- Individual settings -->
        <div style="height:calc(100vh - 180px); overflow: auto;">
            <SimpleGrid  cols={1}>

                <!-- Chatbot choice -->
                <div>
                    <Stack>
                        <Text size='md' weight='semibold' color="blue" style="line-height:1.5">
                            Val av chat
                        </Text>

                        <Text size='sm' weight='semibold' color="blue" style="line-height:1.5">
                            <RadioGroup on:change={updateSettings} bind:value={chatbot_value} items={chatbot_options} color='cyan' size='sm' direction='column' spacing='xs' labelDirection='left'/>
                        </Text>
                    </Stack>
                </div>


                <!-- Language level settings -->
                <div>
                    <Stack>
                        <Text size='md' weight='semibold' color="blue" style="line-height:1.5">Språknivå</Text>

                        <Text size='xs' weight='semibold' color="blue" style="line-height:1.5">
                            <RadioGroup on:change={updateSettings} bind:value={language_value} items={language_options} color='cyan' size='sm' direction='column' spacing='xs' labelDirection='left'/>
                        </Text>
                    </Stack>
                </div>


                <!-- Internet tool setting -->
                <div>
                    <Stack>
                        <Text size='md' weight='semibold' color="blue" style="line-height:1.5">Källor (internet)</Text>
                        
                        <Text size='xs' weight='semibold' color="blue" style="line-height:1.5">
                            <Stack spacing="xs">
                                {#each tool_options as {label,checked}}
                                <Switch {checked} 
                                    on:change={() => 
                                            {
                                                checked = !checked;
                                                updateSettings();
                                            }
                                        }
                                    label={label}
                                    color="cyan"
                                />
                                {/each}
                            </Stack>
                        </Text>
                    </Stack>
                </div>

                <!-- To add more settings, add a div with whatever buttons we want -->
                
            </SimpleGrid>
        </div>
    </Stack>
</div>
{/if}


<style>

    .settings-button {
        position: fixed;
        right: 30px;
        top: 5px;
        z-index: 12;
    }
    .settings-button:hover {
        background-color: #f8f8f8;
        border-radius: 5px;
    }

    .settings-menu {
        background: white;
        position: fixed; 
        top: 80px; 
        right: 0;  
        bottom: 0;
        padding: 20px;
        width: 200px;
        overflow: hidden;
        z-index: 12;
    }

</style>