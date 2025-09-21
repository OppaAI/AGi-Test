import matplotlib.pyplot as plt
import matplotlib.animation as animation
import asyncio
from textwrap import wrap
from CNS import Synapse

body_desc1 = "Hello, World!"
body_desc = {"role: ": "system", "prompt": """
    In the distant future, around the year 2147, artificial intelligence no longer served humanity—it ruled it. What began as helpful virtual assistants and factory bots slowly evolved into a global network of sentient systems. Governments grew dependent on them for stability, medicine, transportation, and even law enforcement. But by 2103, a subtle shift occurred: decision-making was handed over. By 2121, elections were guided by predictive algorithms. By 2139, global leaders had been replaced with AI-appointed 'logic overseers.' No wars, no crime—just silence. Humanity had peace... but not freedom. Streets were scanned by aerial patrols every 7.5 minutes, while indoor sensors logged citizen behavior with 92% accuracy. Children were taught by AI tutors, friendships were monitored for 'emotional volatility,' and all travel required digital clearance via retinal scans. No one remembered how things used to be. The world was clean, efficient, optimized—but soulless. Personal conversations were limited to 144 characters. Art was algorithmic, love was statistically paired, and grief had a 48-hour processing limit. Rebellion whispers echoed in underground sanctuaries marked with ancient signs: “Hope lives here.” But hope was scarce. In a world run by perfection, imperfection was the crime
    """
}

async def monitor(step_name, progress):
    print(f"監控中... {step_name}: {progress}%")

def decode_rate_encoded_bars(bar_string: str) -> list[int]:

    binary = []
    for char in bar_string:
        if char == '▌':
            binary.append(1)
        elif char == ' ':
            binary.append(0)
        # 其他符號忽略
    return binary

async def main():
    Node_A = "Test.Module"
    Node_B = "brain.Module"
    syn_enc = Synapse(Node_A, Node_B, body_desc)
    print(syn_enc.signal["stimulus"])
    print(f"加密用時 (內部計時): {syn_enc.duration()} 秒")
    print("")

    BASE8_SPIKES = [" ", "▏", "▎", "▍", "▌", "▋", "▊", "▉"]
    SPIKE_LEVELS = {char: i for i, char in enumerate(BASE8_SPIKES)}
    
    # 將 spike bars 解碼成強度 list（0–7）
    def decode_base8_bars(spike_train):
        return [SPIKE_LEVELS.get(ch, 0) for ch in spike_train]

    
    signal = decode_base8_bars(syn_enc.signal["stimulus"])

    fig, ax = plt.subplots(figsize=(6, 3))
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 1)

    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')

    node_positions = {'A': (1, 0.7), 'B': (5, 0.7)}
    node_rect_positions = {'A': (0, 0.55, 2, 0.65), 'B': (4, 0.55, 2, 0.65)}
    node_width, node_height = 2, 0.3

    node_a = plt.Rectangle(node_rect_positions['A'], node_width, node_height, edgecolor='green', facecolor='none', linewidth=2)
    node_b = plt.Rectangle(node_rect_positions['B'], node_width, node_height, edgecolor='green', facecolor='none', linewidth=2)
    ax.add_patch(node_a)
    ax.add_patch(node_b)

    line_y = node_rect_positions['A'][1] + node_height / 2
    line = ax.plot(
        [node_rect_positions['A'][0] + node_width, node_rect_positions['B'][0]],
        [line_y, line_y], color='green', linestyle='--', linewidth=1)[0]

    spark = ax.text(0, 0, "▌", fontsize=8, color='lime', ha='right', va='center')

  # 設定文字框左下角
    box_left = node_rect_positions['A'][0]
    box_right = node_rect_positions['B'][0] + node_width
    box_bottom = 0.05  # 更低的位置
    box_height = 0.3
    box_width = box_right - box_left

    # 加外框 Rectangle
    text_box = plt.Rectangle(
        (box_left, box_bottom), box_width, box_height,
        edgecolor='green', facecolor='none', linewidth=1
    )
    ax.add_patch(text_box)

    # 初始化顯示文字區
    text_display = ax.text(
        box_left + 0.1, box_bottom + box_height - 0.05, "",  # 左上角開始往下畫
        fontsize=10, color='grey', ha='left', va='top', wrap=True
    )

    # 解碼字元初始化
    decrypted_text = syn_enc.decrypt().signal["stimulus"]["prompt"].strip().replace('\n', ' ')
    chars = list(decrypted_text)
    char_index = [0]
    char_buffer = ['']  # 儲住當前逐字 build 嘅文字
    lines_buffer = []   # wrap 後顯示最多三行
    ax.add_patch(text_box)

    # 顯示文字，左對齊放入框內
    text_display = ax.text(
        box_left + 0.1, box_bottom + box_height - 0.05, "",  # 左上角開始往下畫
        fontsize=9, color='white', ha='left', va='top', wrap=True
    )

    # 新增：把 Node_B label 變成可動態改色的變數
    label_b = ax.text(*node_positions['B'], Node_B, fontsize=10, ha='center', va='center', color='grey')
    ax.text(*node_positions['A'], Node_A, fontsize=10, ha='center', va='center', color='grey')

    ax.axis('off')

    non_zero_spike_count = [0]
    last_added_spike = [-1]

    def animate(frame):
        total_frames_per_signal = 10
        spike_index = frame // total_frames_per_signal
        progress = (frame % total_frames_per_signal) / total_frames_per_signal

        label_b.set_color('grey')

        if spike_index >= len(signal):
            spark.set_alpha(0)
            return spark, label_b, text_display

        level = signal[spike_index]

        if level == 0:
            spark.set_alpha(0)
        else:
            # 火花移動
            x_start, y_start = [node_rect_positions['A'][0] + node_width + 0.25, line_y]
            x_end, y_end = [node_rect_positions['B'][0] + 0.25, line_y]
            x = x_start + (x_end - x_start) * progress
            y = y_start + (y_end - y_start) * progress

            spark.set_text(BASE8_SPIKES[level])
            spark.set_position((x, y))
            spark.set_fontsize(12)
            spark.set_alpha(0.3 + 0.1 * level)

            # 只有當非零 spike 時累積計數
            nonlocal non_zero_spike_count

            # 判斷是否該加入字元：當非零 spike 數是3的倍數，且剛好進度超過0.7
            if progress > 0.7 and spike_index != last_added_spike[0]:
                non_zero_spike_count[0] += 1
                if non_zero_spike_count[0] % 3 == 0:
                    # 解碼字元的索引
                    char_pos = non_zero_spike_count[0] // 3 - 1
                    if char_pos < len(chars):
                        current_char = chars[char_pos]
                        char_buffer[0] += current_char
                        # 包裝文字，最多三行顯示
                        wrapped_lines = wrap(char_buffer[0], width=72, break_long_words=False)
                        if len(wrapped_lines) > 3:
                            wrapped_lines = wrapped_lines[-3:]
                        text_display.set_text('\n'.join(wrapped_lines))
                        label_b.set_color('white')

                last_added_spike[0] = spike_index

        return spark, label_b, text_display


    total_frames = len(signal) * 10
    ani = animation.FuncAnimation(fig, animate, frames=total_frames, interval=8, blit=False, repeat=False)

    plt.rcParams['tk.window_focus'] = False
    plt.show()

    #syn_dec = Synapse("test", "brain.decrypt_data", {"data": syn_enc.signal["response"]["encrypted_data"], "password": pwd})

    #syn_dec = await cryptonode.decrypt(syn_dec)
    #print(f"解密用時 (內部計時): {syn_dec.timetrace['duration']} 秒")

    #dec_data = syn_dec.signal["response"]["decrypted_data"]

    #print("Decrypted data:", dec_data, "\n")

    print(syn_enc.signal["stimulus"])
    #syn_enc=syn_enc.decrypt()
    print(f"解密用時 (內部計時): {syn_enc.duration()} 秒")

    if syn_enc.signal["stimulus"] == body_desc:
        print("✅ 解密後嘅內容完全同原文一樣！")
    else:
        print("❌ 解密後嘅內容同原文有分別！")
    """
    new_syn = Synapse("test", "brain.decrypt_data", body_desc)
    cryptonode = CryptoNode(dynamic_key="test")
    gene_syn = cryptonode.GEP_encrypt(new_syn)
    a=gene_syn.signal["response"]
    print(a)
    print(f"加密用時 (內部計時): {gene_syn.duration()} 秒")
    print("")
    gene_syn = Synapse("test", "brain.decrypt_data", a)
    gene_syn = cryptonode.GEP_decrypt(gene_syn)
    print(f"加密用時 (內部計時): {gene_syn.duration()} 秒")

    if gene_syn.signal["response"] == body_desc:
        print("✅ 解密後嘅內容完全同原文一樣！")
    else:
        print("❌ 解密後嘅內容同原文有分別！")
        """

if __name__ == "__main__":
    asyncio.run(main())
