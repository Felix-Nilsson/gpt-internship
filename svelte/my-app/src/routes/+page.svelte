<script>
    import { Button, Group, Title } from '@svelteuidev/core';
</script>


<div class="center-screen">
    <!--<iframe 
        title='' src="https://gifer.com/embed/7fpZ" width="100%" height="100%" style='position:absolute;top:0;left:0;'>
    </iframe>-->
    <Group spacing="lg" direction="column">
        <Title order={1} variant='gradient' gradient={{from: 'blue', to: 'red', deg: 45}} style="font-size: 5rem; line-height: 1.5">
            Sahlgrenska AI Hjälp
        </Title>
            <Button href='/login' variant='gradient' gradient={{from: 'teal', to: 'blue', deg: 60}} radius="lg" size="xl" ripple>
                Logga in
            </Button>
    
            <Button href='/chat' variant="outline" radius="lg" size="xl" ripple>
                Internethjälp
            </Button>
        
    </Group>
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


</style>
</head>