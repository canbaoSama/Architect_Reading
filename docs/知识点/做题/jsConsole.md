### 经典面试题

#### this 的指向问题
```js
let length = 20;
let obj = {
    length: 100,
    sayHi() {
        debugger
        console.log(this.length);
    },
};
obj.sayHi();
const fn = obj.sayHi;
fn();

const arr = [obj.sayHi, 2, 3, 4, 5];
arr[0]();
// 输出100 2 5
```

#### 重写 toString()

```js
let a = {
    i: 1,
    toString: function () {
        return a.i++;
    },
};
console.log(a == 1 && a == 2 && a == 3); // true

// 数组
let b = [1, 2, 3];
b.toString = b.shift;
console.log(b == 1 && b == 2 && b == 3); // true
```