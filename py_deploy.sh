#!/usr/bin/env bash
:<<EOF
此脚本用于python3环境的安装部署，依赖NE工具机提供python安装包。
        - 不兼容pyenv
EOF


# web server相关配置
serverIP="172.23.58.119"


# python安装包相关配置
#pyFileName="Python-3.5.5"
pyFileName="Python-3.6.7"
pyFileType=".tar.xz"  # 用于解压缩
pyFile=${pyFileName}${pyFileType}
#pyFileMd5="f3763edf9824d5d3a15f5f646083b6e0"  # Python-3.5.5.tar.xz
pyFileMd5="bb1e10f5cedf21fcf52d2c7e5b963c96"  # Python-3.6.7.tar.xz
pyPath="/export/ne_auto_deploy/py_deploy" # 临时存放文件的地方
installPath="/usr/local/python3"  # 安装路径
# sysPath="/usr/local/bin"  # 部署路径，软链到这里
sysPath="/usr/bin"  # 部署路径，软链到这里


# pip.conf相关配置
pipConfFileName="pip"
pipConfFileType=".conf"  # 用于解压缩
pipConfFile=${pipConfFileName}${pipConfFileType}
pipConfFileMd5="e08a7e1066d771248538bdddb39e9981"
pipConfPath="/etc"


# install openssl-devel, is needed by pip3 and virtualenv.
sudo yum list installed openssl-devel --quiet >/dev/null 2>&1
if [ $? == 0 ]; then
    echo "Need openssl-devel - Completed before"
else
    echo "Need openssl-devel - Installing"
    yum install openssl-devel --quiet --assumeyes >/dev/null 2>&1  # pip 依赖ssl/tls环境
    if [ $? == 0 ]; then
        echo "Install openssl-devel - Finish"
    else
        echo "Install openssl-devel - Failed"
    fi
fi


# 目录创建
if [ ! -d ${pyPath} ]; then
    sudo mkdir -p ${pyPath}
    if [ $? == 0 ]; then
        echo "Create ${pyPath} - Finish"
    else
        echo "Create ${pyPath} - Failed"
    fi
fi


# Download and md5 check -- python3.5.5 后面采用编译安装的方式部署。
retry=3
for i in $(seq 1 ${retry});
do
    if [ ! -f ${pyPath}/${pyFile} ]; then
        sudo curl -o ${pyPath}/${pyFile} http://${serverIP}/${pyFile} --silent
        if [ $? == 0 ]; then
            echo "Download ${pyFile} - Finish"
        else
            echo "Download ${pyFile} - Failed"
        fi
    else
        echo "${pyFile} File exists - Finish"
    fi
    md5_tmp=`sudo md5sum ${pyPath}/${pyFile} | awk '{print $1}'`
    if [ ${md5_tmp} != ${pyFileMd5} ]; then
        echo "MD5 check $pyFile - Failed ${i} time"
        sudo rm -rf "$pyPath/$pyFile"
    else
        echo "MD5 check ${pyFile} - Finish"
        break
    fi
done



# Download and md5 check -- pip.conf 修正了index源，下载package更快速，更稳定。
retry=3
for i in $(seq 1 ${retry});
do
    if [ ! -f ${pipConfPath}/${pipConfFile} ]; then
        sudo curl -o ${pipConfPath}/${pipConfFile} http://${serverIP}/${pipConfFile} --silent
        if [ $? == 0 ]; then
            echo "Download ${pipConfFile} - Finish"
        else
            echo "Download ${pipConfFile} - Failed"
        fi
    else
        echo "${pipConfFile} File exists - Finish"
    fi
    md5_tmp=`sudo md5sum ${pipConfPath}/${pipConfFile} | awk '{print $1}'`
    if [ ${md5_tmp} != ${pipConfFileMd5} ]; then
        echo "MD5 check $pipConfFile - Failed ${i} time"
        sudo rm -rf "$pipConfPath/$pipConfFile"
    else
        echo "MD5 check ${pipConfFile} - Finish"
        break
    fi
done

# Tar
if [ ! -d "$pyPath/$pyFileName" ]; then
    sudo tar xJf "$pyPath"/"$pyFile" -C "$pyPath"
    if [ $? == 0 ]; then
        echo "Tar $pyPath/$pyFile - Finish"
    else
        echo "Tar $pyPath/$pyFile - Failed"
    fi
else
    echo "$pyPath/$pyFileName directory exists "
fi




# Install python3
if [ ! -d "$installPath" ]; then
    # sudo mkdir $installPath 不需要自己会创建
    cd "$pyPath"/"$pyFileName"  # configure,make,make install必须在同一个目录下进行，并会留下无用文件
    # 生产python lib动态库会导致，pip安装package失败
    #./configure --prefix=$installPath --enable-shared >/dev/null 2>&1
    sudo ./configure --prefix="$installPath" >/dev/null 2>&1
    if [ $? == 0 ]; then
        echo "$pyFileName configure - Finish"
    else
        echo "$pyFileName configure - Failed"
    fi
    # sudo ./configure --prefix=/usr/local/python3 --enable-shared --silent
    echo "Please waiting 3 minute for making $pyFileName."
    sudo make >/dev/null 2>&1  # --silent不起用着，重定向到黑洞方式静默
    if [ $? == 0 ]; then
        echo "$pyFileName make - Finish"
    else
        echo "$pyFileName make - Failed"
    fi
    echo "Please waiting 3 minute for installing $pyFileName."
    sudo make install >/dev/null 2>&1
    if [ $? == 0 ]; then
        echo "$pyFileName make install - Finish"
    else
        echo "$pyFileName make install - Failed"
    fi

else
    echo "$installPath directory exists "
fi

# Deploy
sudo ln -s "$installPath"/bin/python3 "$sysPath"/python3

# System path check,pip and virtualenv install.
sudo echo SYSPATH -- $PATH | grep "$sysPath"
if [ $? == 0 ]; then
    sudo ln -s "$installPath"/bin/pip3 "$sysPath"/pip3
    if [ $? == 0 ]; then
        echo "Create link pip - Finish"
    else
        echo "Create link pip - Failed"
    fi
    sudo pip3 install --upgrade pip --quiet
    if [ $? == 0 ]; then
        echo "Upgrade pip - Finish"
    else
        echo "Upgrade pip - Failed"
    fi
    sudo pip3 install virtualenv --quiet
    if [ $? == 0 ]; then
        echo "Install virtualenv - Finish"
    else
        echo "Install virtualenv - Failed"
    fi
    sudo ln -s "$installPath"/bin/virtualenv "$sysPath"/virtualenv3
    if [ $? == 0 ]; then
        echo "Create link virtualenv - Finish"
    else
        echo "Create link virtualenv - Failed"
    fi
else

    echo "Please modify SystemPath, add $sysPath."
fi

:<<EOF
回滚清理
sudo rm -rf /usr/local/python3
sudo rm -rf /export/ne_auto_deploy/py_deploy
sudo rm -rf /export/py_deploy*
sudo rm -rf /usr/bin/pip3
sudo rm -rf /usr/bin/python3
sudo rm -rf /usr/bin/virtualenv3
sudo rm -rf /etc/pip.conf
EOF
