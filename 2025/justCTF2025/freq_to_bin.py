import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, filtfilt
from scipy.fftpack import fft, ifft

def extract_20khz_audio(input_file, output_prefix="segment"):
    # Read the audio file
    sample_rate, audio_data = wavfile.read(input_file)
    
    # Convert to float for processing
    if audio_data.dtype != np.float32:
        audio_data = audio_data.astype(np.float32) / np.iinfo(audio_data.dtype).max
    
    # Design bandpass filter for 20kHz (19.5-20.5kHz range)
    nyquist = sample_rate / 2
    low_freq = 19500 / nyquist
    high_freq = 20500 / nyquist
    
    # Create bandpass filter
    b, a = butter(4, [low_freq, high_freq], btype='band')
    
    # Apply filter
    filtered_audio = filtfilt(b, a, audio_data)
    
    # Split into 0.2 second intervals
    interval_samples = int(0.2 * sample_rate)
    num_segments = len(filtered_audio) // interval_samples
    
    segments = []
    for i in range(num_segments):
        start_idx = i * interval_samples
        end_idx = start_idx + interval_samples
        segment = filtered_audio[start_idx:end_idx]
        segments.append(segment)
    
    print(f"Extracted {len(segments)} segments of 0.2 seconds each")
    return sample_rate, segments

if __name__ == "__main__":
    sample_rate, segments = extract_20khz_audio("challenge.wav")
    bits = []
    for segment in segments:
        # check if there is 20kHz signal in center 0.05 seconds
        center_idx = len(segment) // 2
        segment = segment[center_idx - int(0.05 * sample_rate): center_idx + int(0.05 * sample_rate)]
        fft_segment = fft(segment)
        magnitude = np.abs(fft_segment)
        freq_bins = np.fft.fftfreq(len(segment), d=1/sample_rate)
        if np.mean(magnitude[(freq_bins > 19500) & (freq_bins < 20500)]) > 0.01:
            bits.append(1)
        else:
            bits.append(0)

    # Convert bits to bytes
    byte_array = bytearray()
    for i in range(0, len(bits), 8):
        byte = 0
        for j in range(8):
            if i + j < len(bits):
                byte = (byte << 1) | bits[i + j]
        byte_array.append(byte)

    print(bytes(byte_array).decode('utf-8', errors='ignore'))