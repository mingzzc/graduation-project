<template>
  <el-container>
    <el-header>
      <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal">
  <el-menu-item index="1"><a @click="towelcome()" class="a">网站首页</a></el-menu-item>
  <el-col :span="8" :push="5" class="searcharea">
    <el-input placeholder="请输入书名/作者" clearable v-model="key">
      <el-button @click="search()" slot="append" icon="el-icon-search"></el-button>
    </el-input>
  </el-col>
  <el-menu-item index="2" class="login">{{username}}</el-menu-item>
  <el-menu-item index="3" @click="loginDialogVisable=true" v-show="!iflogin">登录</el-menu-item>
  <el-submenu index="4" v-show="iflogin">
    <template slot="title">个人信息</template>
    <el-menu-item index="2-1" @click="torecommend()">个人主页</el-menu-item>
    <el-menu-item index="2-2" @click="tochangeinfo()">个人资料</el-menu-item>
    <el-menu-item index="2-3" @click="logout()">退出登录</el-menu-item>
  </el-submenu>
  <el-menu-item index="5" @click="registerDialogVisable=true">注册</el-menu-item>
</el-menu>
  </el-header>
    <el-main>
      <router-view></router-view>
    </el-main>
    <el-dialog @close="registerDialogClose" title="注册" :visible.sync="registerDialogVisable" width="30%">
      <el-form ref="registerRef" :model="registerForm" label-width="80px" :rules="registerRules">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="registerForm.username"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="registerForm.password" type="password"></el-input>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="registerForm.email"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer">
        <el-button @click="registerDialogVisable = false">取 消</el-button>
        <el-button type="primary" @click="register">确 定</el-button>
      </span>
    </el-dialog>
    <el-dialog @close="loginDialogClose" title="登录" :visible.sync="loginDialogVisable" width="30%">
      <el-form ref="loginRef" :model="loginForm" label-width="80px" :rules="loginRules">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="loginForm.username"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="loginForm.password" type="password"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer">
        <el-button @click="loginDialogVisable = false">取 消</el-button>
        <el-button type="primary" @click="login">确 定</el-button>
      </span>
    </el-dialog>
    <el-dialog @close="changedinfo" title="个人信息修改" :visible.sync="changeinfovisable" width="30%">
      <el-form ref="changeinfoRef" :model="changeinfoForm" label-width="80px" :rules="changeinfoRules">
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="changeinfo.email"></el-input>
        </el-form-item>
        <el-form-item label="旧密码" prop="oldpassword">
          <el-input v-model="changeinfo.oldpassword" type="password"></el-input>
        </el-form-item>
        <el-form-item label="新密码" prop="newpassword1">
          <el-input v-model="changeinfo.newpassword1" type="password"></el-input>
        </el-form-item>
        <el-form-item label="重复新密码" prop="newpassword2">
          <el-input v-model="changeinfo.newpassword2" type="password"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer">
        <el-button @click="loginDialogVisable = false">取 消</el-button>
        <el-button type="primary" @click="login">确 定</el-button>
      </span>
    </el-dialog>
  </el-container>
</template>

<script>
export default {
  data() {
    //邮箱验证规则
    var checkEmail = (rule, value, cb) => {
      const regEmail = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(\.[a-zA-Z0-9_-])+/;
      if (regEmail.test(value)) return cb();
      cb(new Error("请输入合法的邮箱"));
    };
    return {
      username: '',
      iflogin: false,
      key:'',
      registerDialogVisable: false,
      loginDialogVisable:false,
      changeinfovisable:false,
      registerForm: {
        email: "",
        username: "",
        password: ""
      },
      loginForm:{
        username:'',
        password:''
      },
      changeinfo:{
        email: '',
        oldpassword: '',
        newpassword1: '',
        newpassword2: ''
      },
      //添加注册表单验证对象
      registerRules: {
        username: [
          { required: true, message: "请输入用户名", trigger: "blur" },
          { min: 3, max: 10, message: "长度在3-10之间", trigger: "blur" }
        ],
        password: [
          { required: true, message: "请输入密码", trigger: "blur" },
          { min: 6, max: 15, message: "长度在6-12之间", trigger: "blur" }
        ],
        email: [
          { required: true, message: "请输入邮箱", trigger: "blur" },
          { validator: checkEmail, trigger: "blur" }
        ]
      },
      loginRules: {
        username: [
          { required: true, message: "请输入用户名", trigger: "blur" },
          { min: 3, max: 10, message: "长度在3-10之间", trigger: "blur" }
        ],
        password: [
          { required: true, message: "请输入密码", trigger: "blur" },
          { min: 6, max: 15, message: "长度在6-12之间", trigger: "blur" }
        ]
      }
    };
  },
  created() {
    init()
  },
  methods: {
    registerDialogClose(){
      this.$refs.registerRef.resetFields();
    },
    loginDialogClose(){
      this.$refs.loginRef.resetFields();
    },
    register(){
      this.$refs.registerRef.validate(
        async valid =>{
          if(!valid)return
          var qs = require('qs');
          const  res = await this.$http.post('/api/register',qs.stringify(this.registerForm))
          console.log(res)
          if(res.data==true){
            this.$message.success('注册成功')
            this.registerDialogVisable=false
            this.loginDialogVisable=true
          }
          else{
            this.$message.error('注册失败,请检查用户名或邮箱!')
          }
        }
      )
    },
    login(){
      this.$refs.loginRef.validate(
        async valid =>{
          if(!valid)return
          var qs = require('qs');
          const  res = await this.$http.post('/api/login',qs.stringify(this.loginForm))
          if(res.data.code!==200){
            this.$message.error("网络错误!")
          }
          if(res.data.data.msg=="yes"){
            this.$message.success('登录成功')
            window.sessionStorage.setItem("token",res.data.data.token)
            window.sessionStorage.setItem("username",this.loginForm.username)
            this.iflogin=true
            this.username=this.loginForm.username
            this.loginDialogVisable=false
          }
          else{
            this.$message.error('登录失败,请检查用户名或密码!')
          }
          console.log(res)
        }
      )
    },
    logout(){
      window.sessionStorage.clear()
      this.iflogin=false
      this.username=''
    },
    tochangeinfo(){
      this.changeinfovisable=true
    },
    changedinfo(){

    },
    search(){
      if(this.key == '' )return
      this.$router.push({path:'/search/'+this.key})
      this.$router.go(0)
    },
    towelcome(){
      this.$router.push({path:'/welcome'})
    },
    torecommend(){
      this.$router.push({path:'/recommend'})
    },
    init(){
      const token = window.sessionStorage.getItem("token")
      if(token==null)return
      const username = window.sessionStorage.getItem("username")
      console.log(token)
      this.iflogin=true
      this.username=username
    }
  }
};
</script>

<style scoped>
.el-header {
  margin-bottom: 60px;
  box-shadow: 2px 2px 5px #e9e5e5 !important;
  float: right;
  text-align: center;
}

.el-main {
  margin-left: 10%;
  margin-right: 10%;
}

.searcharea{
  margin-top: 10px;
}

el-head el-button{
  height: 36px !important;
}

.login{
  margin-left: 40% !important;
}

.a{
  text-decoration: none;
}
</style>