import {BarsOutlined, HomeOutlined, NotificationOutlined, SettingOutlined, UserOutlined} from "@ant-design/icons";
import Home from "../pages/home";
import React from "react";
import User from "../pages/user";
import Notify from "../pages/notify";
import Rule from "../pages/rule";
import Setting from "../pages/setting";

export default [
    {
        title: '首页',
        path: '/',
        icon: (<HomeOutlined/>),
        element: (<Home/>),
    },
    {
        title: '规则',
        path: '/rule',
        icon: (<BarsOutlined/>),
        element: (<Rule/>),
    },
    {
        title: '设置',
        type: 'group',
        children: [
            {
                title: '用户',
                path: '/user',
                icon: (<UserOutlined/>),
                element: (<User/>),
                group: '系统'
            },
            {
                title: '通知',
                path: '/notify',
                icon: (<NotificationOutlined/>),
                element: (<Notify/>),
                group: '系统'
            },
            {
                title: '设置',
                path: '/setting',
                icon: (<SettingOutlined/>),
                element: (<Setting/>),
                group: '系统'
            },
        ]
    }
]
