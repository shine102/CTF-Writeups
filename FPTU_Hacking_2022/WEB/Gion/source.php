<?php
error_reporting(0);
highlight_file(__FILE__);

class main{
    public $class;
    public $param;
    public function __construct($class="test",$param="Onion")
    {
        $this->class = $class;
        $this->param = $param;
        echo new $this->class($this->param);
    }
    public function __destruct(){
        echo new $this->class->cc($this->param);
    }

}

class test{
    var $str;
    public function __construct($str)
    {
        $this->str = $str;
        echo ("Welcome to ".$this->str);
    }
}

class do_nothing{
    public $a;
    public $b;
    public function __construct($a,$b){
        $this->a = $a;
        $this->b = $b;
    }
    public function __get($method){
        if(isset($this->a)){
            return $this->b;
        }
        return $method;
    }
}

if(isset($_GET['payload'])){
    unserialize(base64_decode($_GET['payload']));
    throw new Exception("ga");
}
else{
    $main = new main;

}