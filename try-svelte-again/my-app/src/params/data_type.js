/** @type {import('@sveltejs/kit').ParamMatcher} */
export function match(param) {
    if (param == 'input' || param == 'response')
        return true;
    //return /^\d+$/.test(param);
}