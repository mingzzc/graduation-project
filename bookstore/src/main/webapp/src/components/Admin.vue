<template>
  <el-container>
    <el-header>
      <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal">
  <el-menu-item index="1"><a @click="towelcome()" class="a">网站首页</a></el-menu-item>
  <el-col :span="8" :push="5" class="searcharea">
    <el-input placeholder="请输入书名/作者" clearable v-model="query.key">
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
</el-menu>
  </el-header>
    <el-main>
      <div>
        <el-col :span="24">
          <el-card>
             <el-button type="success" @click="addbookvisable=true">添加书籍</el-button>
            <el-table :data="result.bookList">
              <el-table-column label="封面" width="120">
                  <img class="img" src="../assets/imgs/tempimg.jpg">
              </el-table-column>
              <el-table-column label="书名" prop="title" width='250'>
              </el-table-column>
              <el-table-column label="介绍" prop="info" width='750'>
              </el-table-column>
              <el-table-column label="操作" width='120'>
                <template v-slot:default="scope">
                  <el-button @click="edit(scope.row)" type="primary" icon="el-icon-edit" circle></el-button>
                  <el-button @click="deletebook(scope.row)" type="danger" icon="el-icon-delete" circle></el-button>
                </template>
                
              </el-table-column>
            </el-table>
            <el-pagination
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange"
              :page-sizes="[1, 2, 5, 10]"
              :page-size="query.pagesize"
              layout="total, sizes, prev, pager, next, jumper"
              :total="result.num"
            ></el-pagination>
          </el-card>
        </el-col>
      </div>
    </el-main>
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
    <el-dialog @close="editclose" title="书籍信息修改" :visible.sync="editvisable" width="30%">
      <el-form ref="editRef" :model="editbook" label-width="80px">
        <el-form-item label="书名">
          <el-input v-model="editbook.title"></el-input>
        </el-form-item>
        <el-form-item label="作者">
          <el-input v-model="editbook.author"></el-input>
        </el-form-item>
        <el-form-item label="页数">
          <el-input v-model="editbook.pages"></el-input>
        </el-form-item>
        <el-form-item label="装帧">
          <el-input v-model="editbook.bind"></el-input>
        </el-form-item>
        <el-form-item label="价格">
          <el-input v-model="editbook.price"></el-input>
        </el-form-item>
        <el-form-item label="信息">
          <el-input v-model="editbook.info"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer">
        <el-button @click="editvisable = false">取 消</el-button>
        <el-button type="primary" @click="confirmedit">确 定</el-button>
      </span>
    </el-dialog>
        <el-dialog title="添加书籍" :visible.sync="addbookvisable" width="30%">
      <el-form ref="addbookRef" :model="addbook" label-width="80px">
        <el-form-item label="书名">
          <el-input v-model="addbook.title"></el-input>
        </el-form-item>
        <el-form-item label="作者">
          <el-input v-model="addbook.author"></el-input>
        </el-form-item>
        <el-form-item label="页数">
          <el-input v-model="addbook.pages"></el-input>
        </el-form-item>
        <el-form-item label="装帧">
          <el-input v-model="addbook.bind"></el-input>
        </el-form-item>
        <el-form-item label="价格">
          <el-input v-model="addbook.price"></el-input>
        </el-form-item>
        <el-form-item label="信息">
          <el-input v-model="addbook.info"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer">
        <el-button @click="addbookvisable = false">取 消</el-button>
        <el-button type="primary" @click="add">确 定</el-button>
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
      loginDialogVisable:false,
      changeinfovisable:false,
      editvisable:false,
      addbookvisable:false,
      loginForm:{
        username:'',
        password:''
      },
      addbook:{
        title:'',
        author:'',
        pages:0,
        bind:'',
        price:'',
        info:''
      },
      changeinfo:{
        email: '',
        oldpassword: '',
        newpassword1: '',
        newpassword2: ''
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
      },
      query:{
        key:'',
        page:1,
        pagesize:10
      },
      result:{
        bookList:[],
        num:10
      },
      editbook:{
        
      }
    };
  },
  created() {
    init()
  },
  methods: {
    async search(){
      const res = await this.$http.get('api/search',{params:this.query})
      this.result.bookList=res.data.data
      this.result.num=res.data.num
      console.log(this.result)
    },
    handleSizeChange(newsize){
      this.query.pagesize=newsize
      this.search()
    },
    handleCurrentChange(current){
      this.query.page=current
      this.search()
    },
    loginDialogClose(){
      this.$refs.loginRef.resetFields();
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
    towelcome(){
      this.$router.push({path:'/admin'})
    },
    init(){
      const token = window.sessionStorage.getItem("token")
      if(token==null)return
      const username = window.sessionStorage.getItem("username")
      console.log(token)
      this.iflogin=true
      this.username=username
    },
    edit(row){
      this.$confirm('此操作将会改变原记录, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(async () => {
          const t = await this.$http.get("/api/book/"+row.id)
          this.editbook=t.data
          console.log(this.editbook)
          this.editvisable=true
          this.$message({
            type: 'success',
            message: '修改成功，请刷新!'
          });
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消'
          });          
        });
    },
    deletebook(row){
      this.$confirm('此操作将会永久删除本记录, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(async () => {
          this.confirmdelete(row.id)
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消'
          });          
        });
    },
    async confirmedit(id){
      var qs = require('qs');
      const  res = await this.$http.post('/api/edit',qs.stringify(this.editbook))
      if(res.data=='true'){
        this.$message.success("修改成功")
      }
      else{
        this.$message.error("修改失败，请检查网络")
      }
    },
    async confirmdelete(id){
      const res = await this.$http.post('/api/delete?id='+id)
      if(res.data=='true')this.$message.success("删除成功")
      else this.$message.error("网络错误")
    },
    async add(){
      var qs = require('qs');
      const  res = await this.$http.post('/api/add',qs.stringify(this.addbook))
      if(res.data=='true')this.$message.success("添加成功")
      else this.$message.error("网络错误")
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

.img{
  width: 92px;
  height: 120px;
}
</style>