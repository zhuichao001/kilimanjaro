fn variable(){
    let m = 96_000;
    let m = (m+1)/2;
    println!("m={}", m);

    let mut n: u64 = 234;
    n -= 10;
    println!("n={}", n);

    let mut v="yes";
    println!("v={}, len={}", v, v.len());

    v = "no";
    println!("v={}, len={}", v, v.len());

    const PI:f32 = 3.14159;
    println!("PI={}", PI);

    let b: bool = false;
    println!("bool={}", b);

}

fn crash(){
    panic!("crash and burn");
}

fn readfile(){
    use std::fs;
    let filename = String::from("README.md");
    let contents = fs::read_to_string(&filename)
        .expect("Something went wrong reading the file");
    println!("Read file:{}, text:\n{}", filename, contents);
}

fn string(){
    let s = String::new();
    let s2 = String::from("hawk");
    let mut s3 = String::from("hello ");
    let d = 999.to_string();
    let f = 1.2.to_string();
    let birth: u32 = "1984".parse().expect("Not year!");
    s3.push_str("world.");
    println!("{} {} {} {} {} {}", s, s2, s3, d, f, birth);
}

fn ownership(){
    let s1 = String::from("hello");
    let s2 = s1.clone();
    println!("s1={}, s2={}", s1, s2);
    //let s3 = s1;
    //println!("s3={}", s3);
}

fn reference(){
    fn length(s: &String) -> usize {
        s.len()
    }
    let nation = String::from("chinese");
    let len = length(&nation);
    println!("The length of '{}' is {}.", nation, len);
}

fn borrowing(){
    fn change(src: &mut String) {
        src.push_str(", world");
    }
    let mut s = String::from("hello");
    change(&mut s);
    println!("after change:{}", s);

    let r1 = &s;
    let r2 = &s; //SHOULD ERROR
    let r3 = &mut s;
}

fn enumerator(){
    fn first_wordlen(s: &String) -> usize {
       let bytes = s.as_bytes();
       for (i, &item) in bytes.iter().enumerate() {
           if item == b' ' {
               return i;
           }
       }
       s.len()
    }

    let src = String::from("hello world");
    let n = first_wordlen(&src);
    println!("first word len={}", n);
}

fn array(){
    let arr: [u32; 5] = [1, 2, 3, 7, 8];
    for a in arr.iter(){
        println!("{}", a);
    }
}

fn slice(){
    let s = String::from("broadcast");
    let part1 = &s[0..5];
    let part2 = &s[5..9];
    println!("{}={}+{}", s, part1, part2);
}

fn normal_struct(){
    struct Site {
        domain: String,
        found: u32
    };

    let runoob = Site {
        domain: String::from("www.runoob.com"),
        found: 2013
    };
    println!("struct = ({}, {})", runoob.domain, runoob.found);
}

fn tuple_struct(){
    struct Point(f64, f64);
    let pos = Point(0.0, 0.0);
    println!("pos = ({}, {})", pos.0, pos.1);
}

fn tuple(){
    let tup: (i32, f64, u8) = (500, 6.4, 1);
    println!("tuple = ({}, {}, {})", tup.0, tup.1, tup.2);
    let (x, y, z) = tup;
    println!("x={}, y={}, z={}", x, y, z);
}

fn enumer(){
    #[derive(Debug)]
    enum Color {
            Red, Yellow, Blue
    };
    let leaf = Color::Red;
    println!("color={:?}", leaf);
}

fn ifelse(){
    let flag = true;
    let number = if flag {
        9
    } else {
        6
    };
    if !flag {
        println!("false number is: {}", number);
    } else {
        println!("true number is: {}", number);
    }
}

fn looper(){
    let mut counter = 0;
    let res = loop {
        counter += 1;

        if counter == 10 {
            break counter * 2;
        }
    };

    println!("loop result is {}", res);
}

fn module(){
    mod nation {
        pub mod government {
            pub fn run() {println!("nation::government::run");}
        }

        pub mod congress {
            pub fn run() {println!("nation::congress::run");}
        }

        mod court {
            fn run() {
                println!("nation::court::run");
                super::congress::run();
            }
        }
    }
    nation::government::run();
}

fn max(array: &[i32]) -> i32 {
    let mut max_index = 0;
    let mut i = 1;
    while i < array.len() {
        if array[i] > array[max_index] {
            max_index = i;
        }
        i += 1;
    }
    return array[max_index];
}

fn vector(){
    let mut v = vec![1, 2, 4, 8];
    v.push(16);
    println!("{:?}", v);
}

fn hashmap(){
    use std::collections::HashMap;
    let mut map = HashMap::new();
    map.insert("city", "suzhou");
    map.insert("size", "10");
    println!("{}", map.get("city").unwrap());
}

fn oop(){
    pub struct Abs {
        field: i32,
    }

    impl Abs {
        pub fn new(val: i32) -> Abs {
            Abs {
                field: val
            }
        }

        pub fn method(&self) {
            println!("calling public Abs::method");
            self.inner();
        }

        fn inner(&self) {
            println!("calling private Abs::inner");
        }
    }

    let obj = Abs::new(1024);
    obj.method();
}

fn threading(){
    use std::thread;
    use std::time::Duration;

    fn function() {
        for i in 0..5 {
            println!("spawned thread print {}", i);
            thread::sleep(Duration::from_millis(1));
        }
    }

    let handle = thread::spawn(function);
    handle.join().unwrap();
    println!("thread finish.");
}

fn template(){
    #[derive(Debug)]
    struct Point<T> {
        x: T,
        y: T,
    };

    let ipos = Point { x: 6, y: 5 };
    let fpos = Point { x: 30.21, y: 56.03};
    println!("{:?}", ipos);
    println!("{:?}", fpos);
}

fn genericity(){
    trait Comparable { //interface
        fn compare(&self, object: &Self) -> i8;
    }
    fn max<T: Comparable>(array: &[T]) -> &T {
        let mut idx = 0;
        let mut i = 1;
        while i < array.len() {
            if array[i].compare(&array[idx]) > 0 {
                idx = i;
            }
            i += 1;
        }
        &array[idx]
    }
    impl Comparable for i32 {
        fn compare(&self, object: &i32) -> i8 {
            if &self > &object { 1 }
            else if &self == &object { 0 }
            else { -1 }
        }
    }

    let numbers = [3,1,9,2,6,0];
    println!("genericity max={}", max(&numbers));
}


fn main(){
    variable();
    println!("-------------");
    array();
    println!("-------------");
    ownership();
    println!("-------------");
    slice();
    println!("-------------");
    normal_struct();
    println!("-------------");
    tuple_struct();
    println!("-------------");
    tuple();
    println!("-------------");
    enumer();
    println!("-------------");
    module();
    println!("-------------");

    let a = [2, 4, 6, 3, 1];
    println!("max = {}", max(&a));
    println!("-------------");

    vector();
    println!("-------------");
    string();
    println!("-------------");
    hashmap();
    println!("-------------");
    oop();
    println!("-------------");
    threading();
    println!("-------------");
    template();
    println!("-------------");
    genericity();
    println!("-------------");
    ifelse();
    println!("-------------");
    looper();
    println!("-------------");
    reference();
    println!("-------------");
    borrowing();
    println!("-------------");
    enumerator();
    println!("-------------");
    readfile();
    println!("-------------");
}
