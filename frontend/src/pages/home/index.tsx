import {Card, Col, List, Row, Skeleton, Space, Statistic, theme} from "antd";
import React from "react";
import {BarsOutlined, SoundOutlined} from "@ant-design/icons";
import {useRequest} from "ahooks";
import * as api from "../../apis/home";
import dayjs from "dayjs";
import {NotifyItemIcon} from "../notify/item";


function Home() {

    const {
        data: statistics = {},
        loading: statisticsLoading
    } = useRequest(async () => (await api.getStatistics()).data.data)

    const {
        data: schedules = [],
        loading: schedulesLoading
    } = useRequest(async () => (await api.getSchedules()).data.data)

    const {token} = theme.useToken()

    return (
        <Row gutter={[15, 15]}>
            <Col span={24} lg={6}>
                <Space direction={'vertical'} style={{width: '100%', height: '100%'}}>
                    <Card bordered={false} style={{height: 120}} loading={statisticsLoading}>
                        <Statistic
                            title="规则数量"
                            value={statistics.rule_count}
                            prefix={<BarsOutlined/>}
                            suffix="个"
                        />
                    </Card>
                    <Card bordered={false} style={{height: 120}} loading={statisticsLoading}>
                        <Statistic
                            title="今天更新数"
                            value={statistics.today_update}
                            prefix={<SoundOutlined/>}
                            suffix="个"
                        />
                    </Card>
                </Space>
            </Col>
            <Col span={24} lg={8}>
                <Card style={{height: 250, overflow: "scroll"}} title={'任务列表'} loading={schedulesLoading}>
                    <Space direction={'vertical'} style={{width: '100%'}}>
                        {schedules.map((item: any) => (
                            <div style={{display: "flex"}}>
                                <div style={{marginRight: 10, marginTop: 2}}>
                                    <NotifyItemIcon icon={item.favicon} size={30}/>
                                </div>
                                <div>
                                    <div style={{
                                        fontSize: token.fontSizeLG,
                                        fontWeight: token.fontWeightStrong,
                                        color: token.colorText
                                    }}>
                                        {item.title}
                                    </div>
                                    <div style={{
                                        fontSize: token.fontSize,
                                        color: token.colorTextSecondary
                                    }}>
                                        {dayjs(item.next_time).fromNow()}
                                    </div>
                                </div>
                            </div>
                        ))}
                    </Space>
                </Card>
            </Col>
        </Row>
    )
}

export default Home
