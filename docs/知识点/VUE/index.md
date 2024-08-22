### setup 渲染原理

1. 渲染过程中，渲染组件调用 mountComponent 方法初始化组件实例和设置组件实例。
2. 在设置组件实例中，调用 setupComponent 方法，如果是一个有状态组件则调用 setupStatefulComponent 方法来创建渲染上下文代理、判断处理 setup 函数和完成组件实例设置。
3. 首先，在创建渲染上下文代理的流程中，它主要对 instance.ctx 做了代理。在执行组件渲染函数的时候，为了方便用户使用，会直接访问渲染上下文 instance.ctx 中的属性，所以我们也要做一层 proxy，对渲染上下文 instance.ctx 属性的访问和修改，代理到对 setupState、ctx、data、props 中的数据的访问和修改。
4. 如果我们在组件中定义了 setup 函数，接下来就是处理 setup 函数的流程，首先判断 setup 函数的参数长度，如果大于 1，则创建 setupContext 上下文；接着调用 callWithErrorHandling 方法是对 setup 做的一层包装，内部还是执行了 setup，并在有参数的时候传入参数，所以 setup 的第一个参数是 instance.props，第二个参数是 setupContext。函数执行过程中如果有 JavaScript 执行错误就会捕获错误，并执行 handleError 函数来处理；
5. 最后，执行 setup 函数并拿到了返回的结果，那么接下来就要用 handleSetupResult 函数来处理结果，及当 setupResult 是一个对象的时候，我们把它变成了响应式并赋值给 instance.setupState，这样在模板渲染的时候，依据前面的代理规则，instance.ctx 就可以从 instance.setupState 上获取到对应的数据，这就在 setup 函数与模板渲染间建立了联系。
6. 另外当组件没有定义的 setup 的时候，也会执行 finishComponentSetup 函数去完成组件实例的设置。主要做了两件事情：标准化模板或者渲染函数和兼容 Options API

```js
const mountComponent = (initialVNode, container, anchor, parentComponent, parentSuspense, isSVG, optimized) => {
    // 创建组件实例
    const instance = (initialVNode.component = createComponentInstance(initialVNode, parentComponent, parentSuspense));
    // 设置组件实例
    setupComponent(instance);
    // 设置并运行带副作用的渲染函数
    setupRenderEffect(instance, initialVNode, container, anchor, parentSuspense, isSVG, optimized);
};
```

```js
function setupComponent(instance, isSSR = false) {
    const { props, children, shapeFlag } = instance.vnode;
    // 判断是否是一个有状态的组件
    const isStateful = shapeFlag & 4;
    // 初始化 props
    initProps(instance, props, isStateful, isSSR);
    // 初始化 插槽
    initSlots(instance, children);
    // 设置有状态的组件实例
    const setupResult = isStateful ? setupStatefulComponent(instance, isSSR) : undefined;

    return setupResult;
}
```

```js
function setupStatefulComponent(instance, isSSR) {
    const Component = instance.type;
    // 创建渲染代理的属性访问缓存
    instance.accessCache = {};
    // 创建渲染上下文代理
    instance.proxy = new Proxy(instance.ctx, PublicInstanceProxyHandlers);
    // 判断处理 setup 函数
    const { setup } = Component;
    if (setup) {
        // 如果 setup 函数带参数，则创建一个 setupContext
        const setupContext = (instance.setupContext = setup.length > 1 ? createSetupContext(instance) : null);

        // 执行 setup 函数，获取结果
        const setupResult = callWithErrorHandling(setup, instance, 0 /* SETUP_FUNCTION */, [instance.props, setupContext]);

        // 处理 setup 执行结果
        handleSetupResult(instance, setupResult);
    } else {
        // 完成组件实例设置
        finishComponentSetup(instance);
    }
}
```

### 首屏加载时间优化

1. 减小入口文件积
2. 静态资源本地缓存
3. UI 框架按需加载
4. 图片资源的压缩
5. 组件重复打包
6. 开启 GZip 压缩
7. 使用 SSR
8. 资源分包、cdn、压缩
9. 懒加载、图片可渐进式加载
10. 骨架屏提升体验

### 按钮级别的权限控制

-   按钮权限也可以用 v-if 判断：但是如果页面过多，每个页面页面都要获取用户权限 role 和路由表里的 meta.btnPermissions，然后再做判断，这种方式就不展开举例了
-   方案二：通过自定义指令进行按钮权限的判断

### vue3 性能提升优化

1. diff 算法优化： vue3 在 diff 算法中相比 vue2 增加了静态标记
2. 静态提升： 中对不参与更新的元素，会做静态提升，只会被创建一次，在渲染时直接复用
3. 事件监听缓存
4. SSR 优化： 当静态内容大到一定量级时候，会用 createStaticVNode 方法在客户端去生成一个 static node，这些静态 node，会被直接 innerHtml，就不需要创建对象，然后根据对象渲染
