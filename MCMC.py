# number of samples to draw\n",
nsamp=10000\n",
    "\n",
    "# standard deviation of Gaussian proposal\n",
    "sig=1\n",
    "\n",
    "# start point\n",
    "x=-1\n",
    "\n",
    "# data storage\n",
    "X=[]\n",
    "\n",
    "# vector to track the acceptance/rejection rate\n",
    "acc=0\n",
    "rej=0\n",
    "\n",
    "for i in range (1,nsamp+1):\n",
    "    random.seed\n",
    "\n",
    "#    append the number of heads/tails to a list\n",
    "    distrib.append(rand_num)\n",
    "\n",
    "# generate candidate from Gaussian\n",
    "    xd=np.random.normal(x,sig)\n",
    "#    print xd\n",
    "\n",
    "# acceptance probability\n",
    "    accprob=(np.exp(-xd**2)*(2+np.sin(xd*5)+np.sin(xd*2)))/(np.exp(-x**2)*(2+np.sin(x*5)+np.sin(x*2)))\n",
    "#    print accprob\n",
    "    if accprob>1:\n",
    "\n",
    "# new point is the candidate\n",
    "        x=xd; \n",
    "        acc=acc+1\n",
    "    else:\n",
    "#generate random number from 0-1 using uniform distribution\n",
    "        u=random.uniform(0,1)\n",
    "        if u <= accprob:\n",
    "            x=xd\n",
    "            acc=acc+1\n",
    "        else:\n",
    "            x=x\n",
    "            rej=rej+1\n",
    "                        \n",
    "#store the i-th sample\n",
    "    X.append(x) \n",
    "    \n",
    "print ('Acceptance Percentage')\n",
    "print (100*acc/nsamp)\n",
    "\n",
    "#print acc\n",
    "#print rej\n",
    "\n",
    "# plot histogram of the distribution (need to change max/min when using uniform/Chi2)\n",
    "\n",
    "plt.hist(X, range=(-5,5), bins=60, log=False)\n",
    "plt.show()\n",
    "\n",
    "plt.plot(X)\n",