<template>
  <div class="login-container">
    <div>
      <el-form
        ref="loginForm"
        :hidden="hiddleLoginForm"
        :model="loginForm"
        :rules="loginRules"
        class="login-form"
        auto-complete="on"
        label-position="left"
      >
        <div class="title-container">
          <h3 class="title">马鞍山二手房采集与分析系统</h3>
        </div>

        <el-form-item prop="username">
          <span class="svg-container">
            <svg-icon icon-class="user" />
          </span>
          <el-input
            ref="username"
            v-model="loginForm.username"
            placeholder="输入手机号进行登录"
            name="username"
            type="text"
            tabindex="1"
            auto-complete="on"
          />
        </el-form-item>

        <el-form-item prop="password">
          <span class="svg-container">
            <svg-icon icon-class="password" />
          </span>
          <el-input
            :key="passwordType"
            ref="password"
            v-model="loginForm.password"
            :type="passwordType"
            placeholder="密码"
            name="password"
            tabindex="2"
            auto-complete="on"
            @keyup.enter.native="handleLogin"
          />
          <span class="show-pwd" @click="showPwd">
            <svg-icon :icon-class="passwordType === 'password' ? 'eye' : 'eye-open'" />
          </span>
        </el-form-item>

        <el-button
          type="primary"
          style="width:200px;margin-bottom:30px;"
          @click.native.prevent="handleLogin"
        >登录
        </el-button>
        <el-button
          type="primary"
          style="width:200px;margin-bottom:30px;"
          @click.native.prevent="toRegister"
        >注册
        </el-button>
      </el-form>
      <el-form
        ref="registerForm"
        :hidden="hiddleRegisterForm"
        :model="registerForm"
        :rules="registerRules"
        class="login-form"
        auto-complete="on"
        label-position="left"
      >
        <div class="title-container">
          <h3 class="title">欢迎注册</h3>
        </div>
        <el-form-item prop="regPhone">
          <span class="svg-container">
            <svg-icon icon-class="user" />
          </span>
          <el-input
            ref="regPhone"
            v-model="registerForm.regPhone"
            placeholder="请输入手机号进行注册"
            prop="regPhone"
            name="regPhone"
            type="text"
            tabindex="1"
            auto-complete="on"
          />
        </el-form-item>
        <el-form-item prop="regUsername">
          <span class="svg-container">
            <svg-icon icon-class="user" />
          </span>
          <el-input
            ref="regUsername"
            v-model="registerForm.regUsername"
            placeholder="请输入昵称"
            name="regUsername"
            type="text"
            tabindex="1"
            auto-complete="on"
          />
        </el-form-item>
        <el-form-item prop="regPassword">
          <span class="svg-container">
            <svg-icon icon-class="password" />
          </span>
          <el-input
            :key="passwordType"
            ref="regPassword"
            v-model="registerForm.regPassword"
            placeholder="输入密码，长度不能小于6"
            name="password"
            tabindex="2"
            auto-complete="on"
            @keyup.enter.native="handleLogin"
          />
        </el-form-item>
        <el-form-item prop="regPassword2">
          <span class="svg-container">
            <svg-icon icon-class="password" />
          </span>
          <el-input
            :key="passwordType"
            ref="regPassword2"
            v-model="registerForm.regPassword2"
            placeholder="再次输入密码"
            name="password"
            tabindex="2"
            auto-complete="on"
            @keyup.enter.native="handleLogin"
          />
        </el-form-item>
        <el-button
          :loading="loading"
          type="primary"
          style="width:200px;margin-bottom:30px;"
          @click.native.prevent="toLogin"
        >返回
        </el-button>
        <el-button
          :loading="loading"
          type="primary"
          style="width:200px;margin-bottom:30px;"
          @click.native.prevent="handRegister"
        >注册
        </el-button>
      </el-form>
    </div>
  </div>
</template>

<script>

export default {
  name: 'Login',
  data() {
    const validateSex = (rule, value, callback) => {
      if (!['男', '女'].includes(value)) {
        callback(new Error('性能只能为男或女'))
      } else {
        callback()
      }
    }
    const validatePassword = (rule, value, callback) => {
      if (value.length < 6) {
        callback(new Error('长度不能小于6位'))
      } else {
        callback()
      }
    }
    return {
      hiddleLoginForm: false,
      hiddleRegisterForm: true,
      loginForm: {
        username: '',
        password: ''
      },
      loginRules: {
        username: [{ required: true, message: '请输入手机号码', trigger: 'blur' }],
        password: [{ required: true, trigger: 'blur', validator: validatePassword }]
      },
      loading: false,
      passwordType: 'password',
      redirect: undefined,
      registerForm: {
        regPhone: '',
        regUsername: '',
        regPassword: '',
        regPassword2: '',
        regCity: '',
        regSex: '',
        regBirthday: ''
      },
      registerRules: {
        regPhone: [{ required: true, message: '请输入手机号码', trigger: 'blur' }],
        regUsername: [{ required: true, message: '请输入昵称', trigger: 'blur' }],
        regPassword: [{ required: true, trigger: 'blur', validator: validatePassword }],
        regPassword2: [{ required: true, trigger: 'blur', validator: validatePassword }],
        regCity: [{ required: true, message: '请输入所在城市', trigger: 'blur' }],
        regSex: [{ required: true, validator: validateSex, trigger: 'blur' }],
        regBirthday: [{ required: true, message: '请输入生日日期', trigger: 'blur' }]
      }
    }
  },
  watch: {
    $route: {
      handler: function(route) {
        this.redirect = route.query && route.query.redirect
      },
      immediate: true
    }
  },
  methods: {
    toLogin() {
      this.hiddleRegisterForm = true
      this.hiddleLoginForm = false
    },
    toRegister() {
      this.hiddleRegisterForm = false
      this.hiddleLoginForm = true
    },
    showPwd() {
      if (this.passwordType === 'password') {
        this.passwordType = ''
      } else {
        this.passwordType = 'password'
      }
      this.$nextTick(() => {
        this.$refs.password.focus()
      })
    },
    handRegister() {
      this.$refs.registerForm.validate(valid => {
        if (valid) {
          this.loading = true
          this.$store.dispatch('user/register', this.registerForm).then(() => {
            this.$message({
              showClose: true,
              message: '注册成功, 请返回登录！',
              type: 'success'
            })
            // window.location.reload()
            // this.$router.push({path: '/login' })
            this.loading = false
          }).catch(() => {
            this.loading = false
          })
        } else {
          return false
        }
      })
    },
    handleLogin() {
      this.$refs.loginForm.validate(valid => {
        if (valid) {
          this.loading = true
          this.$store.dispatch('user/login', this.loginForm).then(() => {
            this.$router.push({ path: this.redirect || '/' })
            this.loading = false
          }).catch(() => {
            this.loading = false
          })
        } else {
          return false
        }
      })
    }
  }
}
</script>

<style lang="scss">
/* 修复input 背景不协调 和光标变色 */
/* Detail see https://github.com/PanJiaChen/vue-element-admin/pull/927 */

$bg: #283443;
$light_gray: #fff;
$cursor: #fff;

@supports (-webkit-mask: none) and (not (cater-color: $cursor)) {
  .login-container .el-input input {
    color: $cursor;
  }
}

/* reset element-ui css */
.login-container {
  .el-input {
    display: inline-block;
    height: 47px;
    width: 85%;

    input {
      background: transparent;
      border: 0px;
      -webkit-appearance: none;
      border-radius: 0px;
      padding: 12px 5px 12px 15px;
      color: $light_gray;
      height: 47px;
      caret-color: $cursor;

      &:-webkit-autofill {
        box-shadow: 0 0 0px 1000px $bg inset !important;
        -webkit-text-fill-color: $cursor !important;
      }
    }
  }

  .el-form-item {
    border: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(0, 0, 0, 0.1);
    border-radius: 5px;
    color: #454545;
  }
}
</style>

<style lang="scss" scoped>
$bg: #2d3a4b;
$dark_gray: #889aa4;
$light_gray: #eee;

.login-container {
  //min-height: 100%;
  //width: 100%;
  //background-color: $bg;
  //overflow: hidden;
  width: 100%;
  height: 100%;
  background-image: url("../../assets/img/bg.jpg");
  background-size: cover;
  background-position: center;
  position: relative;


  .login-form {
    position: relative;
    width: 520px;
    max-width: 100%;
    padding: 160px 35px 0;
    margin: 0 auto;
    overflow: hidden;
  }

  .tips {
    font-size: 14px;
    color: #fff;
    margin-bottom: 10px;

    span {
      &:first-of-type {
        margin-right: 16px;
      }
    }
  }

  .svg-container {
    padding: 6px 5px 6px 15px;
    color: $dark_gray;
    vertical-align: middle;
    width: 30px;
    display: inline-block;
  }

  .title-container {
    position: relative;

    .title {
      font-size: 26px;
      color: $light_gray;
      margin: 0px auto 40px auto;
      text-align: center;
      font-weight: bold;
    }
  }

  .show-pwd {
    position: absolute;
    right: 10px;
    top: 7px;
    font-size: 16px;
    color: $dark_gray;
    cursor: pointer;
    user-select: none;
  }
}
</style>
