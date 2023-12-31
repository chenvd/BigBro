import React from "react";
import Styles from "./side.module.css";
import {Menu, MenuProps, theme} from "antd";
import routes from "../../routes/routes";
import {useLocation, useNavigate} from "react-router-dom";

type MenuItem = Required<MenuProps>['items'][number];
const {useToken} = theme

interface Props {
    onSelect?: () => void
}

function Sider(props: Props) {

    const {token} = useToken()

    const location = useLocation()
    const navigate = useNavigate()

    function getItem(item: any): any {
        return {
            key: item.path,
            icon: item.icon,
            label: item.title,
            type: item.type,
        }
    }

    function generateItems(routes: any) {
        return routes.map((item: any) => {
            const menuItem = getItem(item)
            if (item.children) {
                menuItem.children = generateItems(item.children)
            }
            return menuItem
        })
    }

    return (
        <div>
            <div className={Styles.logo}>
                <img src="https://gw.alipayobjects.com/zos/rmsportal/KDpgvguMpGfqaHPjicRK.svg" alt=""/>
                <div style={{color: token.colorText}}>BIG BRO</div>
            </div>
            <Menu selectedKeys={[location.pathname]} mode={'inline'} items={generateItems(routes)} onSelect={item => {
                props.onSelect?.()
                navigate(item.key)
            }}/>
        </div>
    )
}

export default Sider
