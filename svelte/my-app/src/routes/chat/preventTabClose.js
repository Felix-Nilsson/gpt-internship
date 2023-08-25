// Taken from: https://svelte.dev/repl/a95db12c1b46433baac2817a0963dc93?version=4.2.0

export const preventTabClose = (_, enabled) => {
    const handler = (e) => {
        e.preventDefault();
        e.returnValue = '';
    }, setHandler = (shouldWork) => shouldWork ?
        window.addEventListener('beforeunload', handler) :
        window.removeEventListener('beforeunload', handler);
    setHandler(enabled);
    return {
        update: setHandler,
        destroy: () => setHandler(false),
    };
};
