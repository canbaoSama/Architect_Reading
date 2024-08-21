function getClientRoot(path) {
    return `${__dirname}${path}`.replace(/\\/g, '/');
}
module.exports = {
    root: true,
    extends: ['@webank/eslint-config-webank/vue.js'],
    overrides: [
        {
            files: ['**/__tests__/*.{j,t}s?(x)', '**/tests/unit/**/*.spec.{j,t}s?(x)'],
        },
    ],
    parserOptions: {
        ecmaFeatures: {
            jsx: true,
            experimentalObjectRestSpread: true,
        },
    },
    settings: {
        'import/resolver': {
            'eslint-import-resolver-custom-alias': {
                alias: {
                    '@': getClientRoot('/src'),
                    '@@': getClientRoot('/src/.fes'),
                },
            },
        },
    },
    env: {
        jest: true,
        node: true,
        'vue/setup-compiler-macros': true, // vue3.2 宏定义报错
    },
    rules: {
        'linebreak-style': [0, 'off', 'windows'],
        'vue/no-multiple-template-root': 'off',
        'import/order': ['error', { 'newlines-between': 'always-and-inside-groups' }], // 修复import 排序问题
    },
};
