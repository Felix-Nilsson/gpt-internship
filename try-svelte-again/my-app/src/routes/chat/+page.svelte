<script>
    import { Group, Title, Paper, ThemeIcon,
         Input , Button, Center, Burger, Navbar, Header,} from '@svelteuidev/core';
    import Icon from '@iconify/svelte';

    let opened = false;
  </script>


<div class="gradient-strip-top">
    <Center style="padding:20px">
        <Title order={1} variant='gradient' gradient={{from: 'blue', to: 'red', deg: 45}} style="font-size: 5rem">
            MedHelp
        </Title>
    </Center>

</div>

<div style="position:fixed; left:30px; top:30px">
    <Burger color="blue"
    {opened}
    on:click={() => (opened = !opened)}
    />
</div>
  
  <div class="center-screen">
    <Group spacing="lg" direction="column">


        <Group spacing="lg" direction="row">
            
            <ThemeIcon variant='gradient' gradient={{from: 'teal', to: 'blue', deg: 45}} size="xl" radius="lg">
                <Icon icon="radix-icons:person" />
            </ThemeIcon>
           
            <Paper shadow="xl" radius="lg">
                <Title order={3} variant='gradient' gradient={{from: 'blue', to: 'teal', deg: 45}} align="left" style="word-wrap;break-word;">
                    Hej, Jag har ont i magen, vad ska jag göra?
                </Title>
              
            </Paper>
        </Group>


        <Group spacing="lg" direction="row">
            
           
            <Paper shadow="xl" radius="lg">
                <Title order={3} variant='gradient' gradient={{from: 'red', to: 'yellow', deg: 45}} align="left">
                    Du borde dricka vatten
                </Title>
              
            </Paper>

            <ThemeIcon variant='gradient' gradient={{from: 'yellow', to: 'red', deg: 45}} size="xl" radius="lg">
                <Icon icon="carbon:bot"/>
            </ThemeIcon>
        </Group>

       
    </Group>
 
</div>

<div class="gradient-strip-bottom">

    <Center style="padding:20px">  
        <Group spacing="lg" direction="row">
                
                <Input 
                variant="filled"
                placeholder="T.ex 'Jag har feber och ont i huvudet, vad borde jag göra?'"
                radius="lg"
                size="xl"
                style="width:20cm"
                />

                <Button color='teal' ripple>Skicka</Button>
            

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
        top:90%; 
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