import pygame
import chess
import chess.engine
import os

class ChessDisplay:
    def __init__(self, screen_size=600, pieces_path=r"C:\Users\Ben\Desktop\die Weiten\Python\Chess\pieceImages"):
        pygame.init()
        self.screen_size = screen_size
        self.square_size = screen_size // 8
        self.screen = pygame.display.set_mode((screen_size, screen_size + 100))
        pygame.display.set_caption("Chess Sharpness")
        
        self.pieces_path = pieces_path
        self.pieces = {}
        self.load_pieces()
        
        self.engine = chess.engine.SimpleEngine.popen_uci(r"C:\Users\Ben\Desktop\die Weiten\Python\Chess\stockfish\stockfish-windows-x86-64-sse41-popcnt.exe")
    
    def load_pieces(self):
        piece_chars = ['K', 'Q', 'R', 'B', 'N', 'P']
        colors = ['w', 'b']
        
        for color in colors:
            for piece in piece_chars:
                filename = f"{color}{piece}.png"
                path = os.path.join(self.pieces_path, filename)
                try:
                    image = pygame.image.load(path)
                    image = pygame.transform.scale(image, (self.square_size, self.square_size))
                    self.pieces[f"{color}{piece}"] = image
                except pygame.error as e:
                    print(f"Error loading piece image {filename}: {e}")
                    print(f"Attempted path: {path}")
                    raise
    
    def get_piece_image(self, piece):
        if piece.symbol().isupper():
            return self.pieces[f"w{piece.symbol()}"]
        else:
            return self.pieces[f"b{piece.symbol().upper()}"]
    
    def calculate_sharpness(self, board):
        """Calculate position sharpness for both sides using multiple factors"""
        if board.is_game_over():
            return (0.0, 0.0)

        try:
            # Factor 1: Evaluation swings from multiple moves
            info = self.engine.analyse(board, chess.engine.Limit(time=0.2), multipv=3)
            
            # Get scores for all analyzed moves
            scores = [entry["score"].relative.score(mate_score=10000)/100 for entry in info]
            
            # Calculate evaluation drops between consecutive moves
            eval_swings = [abs(scores[i] - scores[i+1]) for i in range(len(scores)-1)]
            avg_swing = sum(eval_swings) / len(eval_swings) if eval_swings else 0
            
            # Factor 2: Piece mobility and attack potential
            attack_squares = 0
            defense_needed = 0
            
            # Count attacked squares and pieces needing defense
            for move in board.legal_moves:
                if board.is_capture(move):
                    attack_squares += 1
                    if board.piece_at(move.to_square):
                        defense_needed += 1
            
            # Factor 3: King safety
            king_square = board.king(board.turn)
            king_attackers = len(list(board.attackers(not board.turn, king_square))) if king_square else 0
            
            # Combine factors into final sharpness score
            base_sharpness = (
                min(5, avg_swing * 1.5) +  # Evaluation swings contribute up to 5 points
                min(3, attack_squares * 0.3) +  # Attacks contribute up to 3 points
                min(2, king_attackers * 0.7)  # King safety contributes up to 2 points
            )
            
            # Scale to 0-10
            sharpness = min(10, base_sharpness)
            
            # Adjust based on whose turn it is
            if board.turn == chess.BLACK:
                return (sharpness * 0.8, sharpness)
            else:
                return (sharpness, sharpness * 0.8)
            
        except Exception as e:
            print(f"Error in sharpness calculation: {e}")
            return (0.0, 0.0)
    
    def draw_board(self, board):
        for row in range(8):
            for col in range(8):
                color = (240, 217, 181) if (row + col) % 2 == 0 else (181, 136, 99)
                pygame.draw.rect(self.screen, color, 
                               (col * self.square_size, row * self.square_size, 
                                self.square_size, self.square_size))
        
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                row = 7 - chess.square_rank(square)
                col = chess.square_file(square)
                piece_image = self.get_piece_image(piece)
                self.screen.blit(piece_image, 
                               (col * self.square_size, row * self.square_size))
    
    def get_evaluation(self, board):
        if board.is_game_over():
            return "Game Over"
        
        info = self.engine.analyse(board, chess.engine.Limit(time=0.1))
        score = info["score"].relative.score(mate_score=10000)
        depth = info["depth"]  # Get the search depth from the analysis
        
        eval_text = f"Evaluation: {score/100:+.2f} ({depth})"
        return eval_text
    
    
    def display_position(self, fen):
        board = chess.Board(fen)
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            self.screen.fill((255, 255, 255))
            self.draw_board(board)
            
            # Display evaluation and depth
            eval_text = self.get_evaluation(board)
            font = pygame.font.Font(None, 36)
            eval_surface = font.render(eval_text, True, (0, 0, 0))
            eval_rect = eval_surface.get_rect(center=(self.screen_size/2, self.screen_size + 25))
            self.screen.blit(eval_surface, eval_rect)
            
            # Display sharpness
            white_sharpness, black_sharpness = self.calculate_sharpness(board)
            sharpness_text = f"Sharpness - W: {white_sharpness:.1f} B: {black_sharpness:.1f}"
            sharp_text = font.render(sharpness_text, True, (0, 0, 0))
            sharp_rect = sharp_text.get_rect(center=(self.screen_size/2, self.screen_size + 75))
            self.screen.blit(sharp_text, sharp_rect)
            
            pygame.display.flip()
        
        self.engine.quit()
        pygame.quit()

def main():
    display = ChessDisplay()
    # Sicilian Dragon position
    sharp_fen = "rnb1kb1r/1p3pp1/p2ppn1p/4P1B1/3N1P2/q1N5/P1PQ2PP/1R2KB1R w Kkq - 0 11" 
    calm_fen  = "rnbq1rk1/p4ppp/1ppbpn2/3p4/3P4/2PBPNB1/PP2QPPP/RN2K2R b KQ - 1 8"
    start     = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    display.display_position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

if __name__ == "__main__":
    main()
