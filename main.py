import pygame
from policy_gradient import network
from abstract import abstract




env=abstract()

#----パラメータの調整--------

#ノード数のパラメータ
agent=network(10,20,5)

#---------------------------
reward_sum=0
running_reward = None
prev_x = 0
episode=0
observation=env.reset()

while True:
    env.render()
    cur_x=observation
    x = [0] * 10
    x[cur_x] = 1
    x[5+prev_x] = 1
    prev_x = cur_x
    aprob=agent.forward(x)
    action = agent.select_action(aprob)
    observation,reward,done=env.step(action)
    reward_sum += reward
    agent.record_reward(reward)

    if done:
        episode+=1
        if reward_sum != 0:
            agent.backward()
        if episode%10==0:
            agent.update()

        #running_rewardの中身が空なら累計した報酬をそのまま保管し、そうでなければ移動平均を求める
        running_reward = reward_sum if running_reward is None \
                         else running_reward * 0.99 + reward_sum * 0.01
        print ('resetting env. episode reward total was %f. running mean: %f'
               % (reward_sum, running_reward))


        #100回行動した後の処理を終えたら累積した報酬と環境をリセット
        reward_sum = 0
        observation=env.reset() # reset env

    if reward != 0: # Pong has either +1 or -1 reward exactly when game ends.
        print (('ep %d: game finished, reward: %f'
              % (episode, reward)) + \
             ('' if reward == -1 else ' !!!!!!!!'))

    pygame.display.update()

pygame.quit()
