<template>
  <div class="app-container">
    <el-form ref="form" :model="form" :rules="rules" label-width="150px" style="width: 600px">
      <el-form-item label="原密码：" prop="password">
        <el-input v-model="form.password" />
      </el-form-item>
      <el-form-item label="新密码：" prop="password">
        <el-input v-model="form.newPassword" />
      </el-form-item>
      <el-form-item label="确认新密码：" prop="password">
        <el-input v-model="form.newPassword2" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handModify">确认修改</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  data() {
    const validatePassword = (rule, value, callback) => {
      if (value.length < 6) {
        callback(new Error('长度不能小于6位'))
      } else {
        callback()
      }
    }
    return {
      form: {
        password: '',
        newPassword: '',
        newPassword2: '',
        userName: '',
        birthday: '',
        sex: '',
        city: ''
      },
      rules: {
        password: [{ required: true, trigger: 'blur', validator: validatePassword }]
      }
    }
  },
  methods: {
    onSubmit() {
      this.$message('submit!')
    },
    handModify() {
      this.$refs.form.validate(valid => {
        if (valid) {
          this.loading = true
          this.$store.dispatch('user/modify', this.form).then(() => {
            this.$message.success('修改成功，下次登录生效！')
            this.loading = false
          }).catch(() => {
            this.loading = false
          })
        } else {
          return false
        }
      })
    },
    onCancel() {
      this.$message({
        message: 'cancel!',
        type: 'warning'
      })
    }
  }
}
</script>

<style scoped>
.line{
  text-align: center;
}
</style>

