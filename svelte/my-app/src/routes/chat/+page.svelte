<script>
    import { Group, Title, Paper, ThemeIcon,
         Input , Button, Center, Burger, Navbar, Header,} from '@svelteuidev/core';
    import Icon from '@iconify/svelte';
    import Conversation from "./Conversation.svelte";

    let opened = false;

    //Backend should be running on port 5001
    const DATA_URL = 'http://localhost:5001/data';

    let check;

    async function get_response() {
        check();
    }

    const handleSubmit = e => {

        //data contains the input
        let data = new FormData(e.target);

        fetch(DATA_URL, {
            method: "POST",
            body: JSON.stringify({'prompt': data.get('prompt')}),
            headers: {"Content-type": "application/json; charset=UTF-8"}
        });

		//Start looking for a response
		get_response();
	}


</script>


<div class="gradient-strip-top">
    <Center style="padding:20px">
        <Button href='/' color=white>
            <Title order={1} variant='gradient' gradient={{from: 'blue', to: 'red', deg: 45}} style="font-size: 5rem">
                MedHelp
            </Title>
        </Button>
    </Center>

</div>

<div style="position:fixed; left:30px; top:30px">
    <Burger color="blue"
    {opened}
    on:click={() => (opened = !opened)}
    />
</div>  
    <div class="center-screen">
    <Conversation bind:check_for_messages={check}></Conversation>
</div>


<div class="gradient-strip-bottom">

    <Center style="padding:20px">  
        <Group spacing="lg" direction="row">
                
                <form on:submit|preventDefault={handleSubmit}>
                    <Group spacing="lg" direction="row">
                        <Input 
                            name="prompt"
                            variant="filled"
                            placeholder="T.ex 'Jag har feber och ont i huvudet, vad borde jag göra?'"
                            radius="lg"
                            size="xl"
                            style="width:20cm"
                        />
                        <Button type="submit" color='teal' ripple>Skicka</Button>
                    </Group>
                </form>

                
            

        </Group>
    </Center>
</div>




<head>
    <style>
        .center-screen {
      display: flex;
      justify-content: center;
      align-items: center;
      text-align: center;
      min-height: 100vh;
    }
    
        .button {
      padding-top: 50px;
      padding-right: 30px;
      padding-bottom: 50px;
      padding-left: 80px;
    }

        .bottom {
      display: flex;
      justify-content: bottom;
      align-items: bottom;
      text-align: bottom;
      min-height: 100vh;
    }

    
    .gradient-strip-bottom {
        background: rgb(34,193,195);
        background: linear-gradient(45deg, rgba(34,193,195,1) 0%, rgba(0,80,200,1) 50%, rgba(34,193,195,1) 100%);
        position: fixed; 
        bottom: 0; 
        left: 0; 
        right: 0; 
        top:100% - 100px; 
    }

    .gradient-strip-top {
        /*background: rgb(34,193,195);
        background: linear-gradient(45deg, rgba(34,193,195,1) 0%, rgba(0,80,200,1) 50%, rgba(34,193,195,1) 100%);*/
        color:white;
        position: fixed; 
        top: 0; 
        left: 0; 
        right: 0; 
        bottom:90%; 
    }
    
    
    </style>
</head>