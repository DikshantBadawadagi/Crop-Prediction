export default {
    root: {
        class: [
            //Shape
            'rounded-md',
            'shadow-md',

            //Color
            'bg-surface-100 dark:bg-surface-800',
            'text-surface-700 dark:text-surface-0'
        ]
    },
    body: {
        class: 'p-0'
    },
    title: {
        class: 'text-2xl font-bold'
    },
    subtitle: {
        class: [
            //Font
            'font-normal',

            //Spacing
            'mb-0',

            //Color
            'text-surface-600 dark:text-surface-0/60'
        ]
    },
    content: {
        class: 'py-0' // Vertical padding.
    },
    footer: {
        class: 'pt-5' // Top padding.
    }
};
