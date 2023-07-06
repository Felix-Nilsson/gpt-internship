<script>
    import { Input, InputWrapper, Title, Group, Button } from '@svelteuidev/core';
    import { EnvelopeClosed,LockClosed } from 'radix-icons-svelte';
  </script>
  
  

   <div class="center-screen">
    <Group spacing="lg" direction="column">
        <Title order={1} variant='gradient' gradient={{from: 'blue', to: 'red', deg: 45}} style="font-size: 5rem">
            MedHelp
        </Title>
        
        <Input icon={EnvelopeClosed} 
            placeholder="Personnummer"
            radius="lg"
            size="xl"
        />

        <Input 
            type="password" 
            icon={LockClosed} 
            placeholder="Lösenord"
            radius="lg"
            size="xl"
        />

        <Button variant='gradient' gradient={{from: 'teal', to: 'blue', deg: 60}} radius="lg" size="xl" ripple>
            Skicka
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