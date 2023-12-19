import {theme} from "antd";
import TelegramIcon from "../assets/icon/telegram.png";
import Webhook from "../assets/icon/webhook.png";
import NotifyTypeTelegram from "../pages/notify/types/telegram";
import NotifyTypeWebhook from "../pages/notify/types/webhook";
import {ReactElement} from "react";


export const themes = [
    {name: 'default', algorithm: theme.defaultAlgorithm, icon: 'icon-light-mode'},
    {name: 'dark', algorithm: theme.darkAlgorithm, icon: 'icon-dark-mode'},
]


export const notifies: {
    [key: string]: { name: string, description: string, icon: string, form: () => ReactElement }
} = {
    telegram: {name: 'telegram', description: 'Telegram', icon: TelegramIcon, form: NotifyTypeTelegram},
    webhook: {name: 'webhook', description: 'Web Hook', icon: Webhook, form: NotifyTypeWebhook},
}
