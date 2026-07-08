package dev.gacastelo.felichia.exceptions;

import jakarta.servlet.http.HttpServletRequest;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.time.Instant;
import java.util.List;

@RestControllerAdvice
public class TratadorGlobalException {

    @ExceptionHandler(NaoEncontradoException.class)
    public ResponseEntity<ErroApi> tratarNaoEncontrado(NaoEncontradoException ex, HttpServletRequest request) {
        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(
                new ErroApi(Instant.now(), 404, "Não Encontrado", ex.getMessage(), request.getRequestURI(), List.of())
        );
    }

    @ExceptionHandler(IllegalStateException.class)
    public ResponseEntity<ErroApi> tratarIllegalState(IllegalStateException ex, HttpServletRequest request) {
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(
                new ErroApi(Instant.now(), 400, "Requisição Inválida", ex.getMessage(), request.getRequestURI(), List.of())
        );
    }

    @ExceptionHandler(IllegalArgumentException.class)
    public ResponseEntity<ErroApi> tratarIllegalArgument(IllegalArgumentException ex, HttpServletRequest request) {
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(
                new ErroApi(Instant.now(), 400, "Requisição Inválida", ex.getMessage(), request.getRequestURI(), List.of())
        );
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErroApi> tratarValidacao(MethodArgumentNotValidException ex, HttpServletRequest request) {
        List<ErroApi.ErroCampo> campos = ex.getBindingResult().getFieldErrors().stream()
                .map(fe -> new ErroApi.ErroCampo(fe.getField(), fe.getDefaultMessage()))
                .toList();
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(
                new ErroApi(Instant.now(), 400, "Requisição Inválida", "Erro Validacao", request.getRequestURI(), campos)
        );
    }

    @ExceptionHandler(VersaoDesatualizadaException.class)
    public ResponseEntity<ErroApi>tratarVersaoDesatualizada(Exception ex, HttpServletRequest request) {
        return ResponseEntity.status(HttpStatus.CONFLICT).body(
                new ErroApi(Instant.now(), 409, "Conflito de versões", ex.getMessage(), request.getRequestURI(), List.of())
        );
    }

    @ExceptionHandler(AccessDeniedException.class)
    public ResponseEntity<ErroApi> tratarAccessDenied(AccessDeniedException ex, HttpServletRequest request) {
        return ResponseEntity.status(HttpStatus.FORBIDDEN).body(
                new ErroApi(Instant.now(), 403, "Acesso Negado", ex.getMessage(), request.getRequestURI(), List.of())
        );
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErroApi> tratarException(Exception ex, HttpServletRequest request) {
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(
                new ErroApi(Instant.now(), 500, "Erro Interno", ex.getMessage(), request.getRequestURI(), List.of())
        );
    }
}
