<template>
  <div class="app-container">
    <el-row style="margin: 10px">
      <el-button type="primary" @click="start">启动采集</el-button>
      <el-button type="warning" @click="stop">关闭采集</el-button>
    </el-row>
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span>采集日志</span>
      </div>
      <div v-for="(item, o) in logs" :key="o" class="text item">
        {{item}}
      </div>
    </el-card>

  </div>
</template>

<script>
// eslint-disable-next-line no-unused-vars
import { startCrawler, stopCrawler, getCrawlerLog } from '@/api/house'

export default {
  data() {
    return {
      logs: []
    }
  },
  mounted() {
    this.setRequestTimer()
  },
  beforeDestroy() {
    this.clearRequestTimer()
  },
  methods: {
    clearRequestTimer() {
      clearInterval(this.requestTimer)
      this.requestTimer = null
    },
    setRequestTimer() {
      this.requestTimer = setInterval(() => {
        this.getLog()
      }, 3000)
    },
    start() {
      startCrawler().then(response => {
        this.$message.success('下发成功')
        this.getLog()
      })
    },
    stop() {
      stopCrawler().then(response => {
        this.$message.success('停止成功')
      })
    },
    getLog() {
      getCrawlerLog().then(response => {
        this.logs = response.data
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

